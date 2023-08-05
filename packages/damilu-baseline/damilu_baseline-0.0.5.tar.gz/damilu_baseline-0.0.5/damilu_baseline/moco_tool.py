# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import random
from PIL import ImageFilter

import torch
import torch.nn as nn
import torchvision.models as models


class MoCo(nn.Module):
    """
    Build a MoCo model with: a query encoder, a key encoder, and a queue
    https://arxiv.org/abs/1911.05722
    """

    def __init__(self, base_encoder, dim:int, K:int, m:float, T:float, infoNCE:int, HX:int):
        """
        dim: feature dimension (default: 128)
        K: queue size; number of negative keys (default: 65536)
        m: moco momentum of updating key encoder (default: 0.999)
        T: softmax temperature (default: 0.07)
        """
        super(MoCo, self).__init__()

        self.K = K
        self.m = m
        self.T = T
        self.infoNCE = infoNCE
        self.HX = HX

        # create the encoders
        # num_classes is the output fc dimension
        self.online_network = base_encoder(num_classes=dim)
        self.target_network = base_encoder(num_classes=dim)

        dim_mlp = self.online_network.fc.weight.shape[1]
        self.online_network.fc = nn.Sequential(nn.Linear(dim_mlp, dim_mlp), nn.ReLU(), self.online_network.fc)
        self.target_network.fc = nn.Sequential(nn.Linear(dim_mlp, dim_mlp), nn.ReLU(), self.target_network.fc)

        for param_q, param_k in zip(self.online_network.parameters(), self.target_network.parameters()):
            param_k.data.copy_(param_q.data)  # initialize
            param_k.requires_grad = False  # not update by gradient

        # create the queue
        self.register_buffer("queue", torch.randn(dim, K))
        self.queue = nn.functional.normalize(self.queue, dim=0)

        self.register_buffer("queue_ptr", torch.zeros(1, dtype=torch.long))

    def __call__(self, im_q, im_k):
        """
        Input:
            im_q: a batch of query images
            im_k: a batch of key images
        Output:
            logits, targets
        """

        # compute query features
        self.online_network.avgpool.register_forward_hook(get_activation('online_network.0projector'))
        self.online_network.fc[0].register_forward_hook(get_activation('online_network.1linear'))
        q_out = self.online_network(im_q)  # queries: NxC
        q_1linear = torch.squeeze(activation['online_network.1linear'])
        q_gap = torch.squeeze(activation['online_network.0projector'])
        if self.infoNCE == 0:
            q = nn.functional.normalize(q_gap, dim=1)
        elif self.infoNCE == 1:
            q = nn.functional.normalize(q_1linear, dim=1)
        elif self.infoNCE == 2:
            q = nn.functional.normalize(q_out, dim=1)

        # compute key features
        with torch.no_grad():  # no gradient to keys
            self._momentum_update_key_encoder()  # update the key encoder

            # # shuffle for making use of BN
            # im_k, idx_unshuffle = self._batch_shuffle_ddp(im_k)

            self.target_network.avgpool.register_forward_hook(get_activation('target_network.0projector'))
            self.target_network.fc[0].register_forward_hook(get_activation('target_network.1linear'))
            k_out = self.target_network(im_k)  # keys: NxC
            k_1linear = torch.squeeze(activation['online_network.1linear'])
            k_gap = torch.squeeze(activation['online_network.0projector'])
            if self.infoNCE == 0:
                k = nn.functional.normalize(k_gap, dim=1)
            elif self.infoNCE == 1:
                k = nn.functional.normalize(k_1linear, dim=1)
            elif self.infoNCE == 2:
                k = nn.functional.normalize(k_out, dim=1)

            # # undo shuffle
            # k = self._batch_unshuffle_ddp(k, idx_unshuffle)

        # compute logits
        # Einstein sum is more intuitive
        # positive logits: Nx1
        l_pos = torch.einsum('nc,nc->n', [q, k]).unsqueeze(-1)
        # negative logits: NxK
        l_neg = torch.einsum('nc,ck->nk', [q, self.queue.clone().detach()])

        # logits: Nx(1+K)
        logits = torch.cat([l_pos, l_neg], dim=1)

        # apply temperature
        logits /= self.T

        # labels: positive key indicators
        labels = torch.zeros(logits.shape[0], dtype=torch.long).cuda()

        # dequeue and enqueue
        self._dequeue_and_enqueue(k)

        if self.HX == 0:
            return logits, labels, q_gap
        elif self.HX == 1:
            return logits, labels, q_1linear
        elif self.HX == 2:
            return logits, labels, q_out
        else:
            return logits, labels, q_out


    @torch.no_grad()
    def _momentum_update_key_encoder(self):
        """
        Momentum update of the key encoder
        """
        for param_q, param_k in zip(self.online_network.parameters(), self.target_network.parameters()):
            param_k.data = param_k.data * self.m + param_q.data * (1. - self.m)

    @torch.no_grad()
    def _dequeue_and_enqueue(self, keys):
        # # gather keys before updating queue
        # keys = concat_all_gather(keys)

        batch_size = keys.shape[0]

        ptr = int(self.queue_ptr)
        assert self.K % batch_size == 0  # for simplicity

        # replace the keys at ptr (dequeue and enqueue)
        self.queue[:, ptr:ptr + batch_size] = keys.T
        ptr = (ptr + batch_size) % self.K  # move pointer

        self.queue_ptr[0] = ptr

#     @torch.no_grad()
#     def _batch_shuffle_ddp(self, x):
#         """
#         Batch shuffle, for making use of BatchNorm.
#         *** Only support DistributedDataParallel (DDP) model. ***
#         """
#         # gather from all gpus
#         batch_size_this = x.shape[0]
#         x_gather = concat_all_gather(x)
#         batch_size_all = x_gather.shape[0]
#
#         num_gpus = batch_size_all // batch_size_this
#
#         # random shuffle index
#         idx_shuffle = torch.randperm(batch_size_all).cuda()
#
#         # broadcast to all gpus
#         torch.distributed.broadcast(idx_shuffle, src=0)
#
#         # index for restoring
#         idx_unshuffle = torch.argsort(idx_shuffle)
#
#         # shuffled index for this gpu
#         gpu_idx = torch.distributed.get_rank()
#         idx_this = idx_shuffle.view(num_gpus, -1)[gpu_idx]
#
#         return x_gather[idx_this], idx_unshuffle
#
#     @torch.no_grad()
#     def _batch_unshuffle_ddp(self, x, idx_unshuffle):
#         """
#         Undo batch shuffle.
#         *** Only support DistributedDataParallel (DDP) model. ***
#         """
#         # gather from all gpus
#         batch_size_this = x.shape[0]
#         x_gather = concat_all_gather(x)
#         batch_size_all = x_gather.shape[0]
#
#         num_gpus = batch_size_all // batch_size_this
#
#         # restored index for this gpu
#         gpu_idx = torch.distributed.get_rank()
#         idx_this = idx_unshuffle.view(num_gpus, -1)[gpu_idx]
#
#         return x_gather[idx_this]
#
#
# # utils
# @torch.no_grad()
# def concat_all_gather(tensor):
#     """
#     Performs all_gather operation on the provided tensors.
#     *** Warning ***: torch.distributed.all_gather has no gradient.
#     """
#     tensors_gather = [torch.ones_like(tensor)
#                       for _ in range(torch.distributed.get_world_size())]
#     torch.distributed.all_gather(tensors_gather, tensor, async_op=False)
#
#     output = torch.cat(tensors_gather, dim=0)
#     return output


class TwoCropsTransform:
    """Take two random crops of one image as the query and key."""

    def __init__(self, base_transform):
        self.base_transform = base_transform

    def __call__(self, x):
        q = self.base_transform(x)
        k = self.base_transform(x)
        return [q, k]


class GaussianBlur(object):
    """Gaussian blur augmentation in SimCLR https://arxiv.org/abs/2002.05709"""

    def __init__(self, sigma=[.1, 2.]):
        self.sigma = sigma

    def __call__(self, x):
        sigma = random.uniform(self.sigma[0], self.sigma[1])
        x = x.filter(ImageFilter.GaussianBlur(radius=sigma))
        return x


activation = {}
def get_activation(name):
    def hook(model, input, output):
        activation[name] = output
    return hook


if __name__ == '__main__':
    model_names = sorted(name for name in models.__dict__
                         if name.islower() and not name.startswith("__")
                         and callable(models.__dict__[name]))

    model = MoCo(models.__dict__['resnet18'], 128, 1024, 0.999, 0.5, 2, 0).to(torch.device('cpu'))
    print(model.online_network.avgpool)
    print(model.online_network.fc)