import os
import time
import yaml
import shutil
import random
from PIL import Image
from PIL import ImageFilter

# -*-coding:utf-8-*-
import torch
import torchvision
import torch.nn as nn
import torchvision.models as models
from torch.utils.data import Dataset
from torchvision import transforms as TF


class dataset_SimCLR(Dataset):
    def __init__(self, root):
        self.root = root
        self.imgs_path = self.get_img_paths(root)
        self.transform = TF.Compose(
            [
                TF.Grayscale(3),
                TF.RandomResizedCrop(64, scale=(0.85, 1.0)),
                TF.RandomHorizontalFlip(),
                TF.RandomApply([TF.RandomRotation(30)], p=0.2),
                TF.RandomApply([TF.ColorJitter(0.4, 0.4, 0.4)], p=0.4),
                TF.ToTensor(),
                TF.RandomApply([GaussianNoise()], p=0.2),
                TF.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
            ]
        )

    def __len__(self):
        return len(self.imgs_path)

    def __getitem__(self, item):
        start_time = time.perf_counter()
        path = self.imgs_path[item]
        with open(path, 'rb') as f:
            with Image.open(f) as origin_img:
                origin_img = origin_img.convert('RGB')  ## 如果不使用，convert('RGB')进行转换的话，读出来的图像是RGBA四通道的，A通道为透明通道
                # print('origin_img', origin_img)

        if self.transform is not None:
            img_i = self.transform(origin_img)
            img_j = self.transform(origin_img)

            end_time = time.perf_counter()
            # print('end_time - start_time', end_time - start_time)
            return img_i, img_j

    def get_img_paths(self, root):
        imgs = []
        for subset in os.listdir(root):
            subset_path = os.path.join(root, subset)
            for img_name in os.listdir(subset_path):
                imgs.append(os.path.join(subset_path, img_name))
        random.shuffle(imgs)
        return imgs


class GaussianBlur(object):
    """Gaussian blur augmentation in SimCLR_80% https://arxiv.org/abs/2002.05709"""

    def __init__(self, sigma=[.4, 2.]):
        self.sigma = sigma

    def __call__(self, x):
        sigma = random.uniform(self.sigma[0], self.sigma[1])
        x = x.filter(ImageFilter.GaussianBlur(radius=0.5))
        return x


class GaussianNoise(object):
    """Gaussian Noise Augmentation for tensor"""

    def __init__(self, sigma=0.1):
        self.sigma = sigma

    def __call__(self, img):
        noise = torch.randn(1, img.shape[1], img.shape[2])
        noise = torch.cat([noise, noise, noise], dim=0)
        return torch.clamp(img + self.sigma * noise, 0.0, 1.0)


class BaseSimCLRException(Exception):
    """Base exception"""


class InvalidBackboneError(BaseSimCLRException):
    """Raised when the choice of backbone Convnet is invalid."""


class InvalidDatasetSelection(BaseSimCLRException):
    """Raised when the choice of dataset is invalid."""


class model_Pretrian(nn.Module):

    def __init__(self, base_model, linear1_out, linear2_out):
        super(model_Pretrian, self).__init__()
        self.resnet_dict = {"resnet18": models.resnet18(pretrained=False, num_classes=128),
                            "resnet50": models.resnet50(pretrained=False, num_classes=128)}

        self.backbone = self._get_basemodel(base_model)
        dim_mlp = self.backbone.fc.in_features

        # add mlp projection head
        self.backbone.fc = nn.Sequential(nn.Linear(dim_mlp, linear1_out), nn.ReLU(), nn.Linear(linear1_out, linear2_out))

    def _get_basemodel(self, model_name):
        try:
            model = self.resnet_dict[model_name]
        except KeyError:
            raise InvalidBackboneError(
                "Invalid backbone architecture. Check the config file and pass one of: resnet18 or resnet50")
        else:
            return model

    def forward(self, x):
        return self.backbone(x)


class model_SimCLR(nn.Module):

    def __init__(self, base_model, out_dim):
        super(model_SimCLR, self).__init__()
        self.resnet_dict = {"resnet18": models.resnet18(pretrained=False, num_classes=out_dim),
                            "resnet50": models.resnet50(pretrained=False, num_classes=out_dim)}

        self.backbone = self._get_basemodel(base_model)
        dim_mlp = self.backbone.fc.in_features

        # add mlp projection head
        self.backbone.fc = nn.Sequential(nn.Linear(dim_mlp, 2 * dim_mlp), nn.ReLU(), nn.Linear(2 * dim_mlp, out_dim))

    def _get_basemodel(self, model_name):
        try:
            model = self.resnet_dict[model_name]
        except KeyError:
            raise InvalidBackboneError(
                "Invalid backbone architecture. Check the config file and pass one of: resnet18 or resnet50")
        else:
            return model

    def forward(self, x):
        return self.backbone(x)


class model_BIDFC(nn.Module):
    def __init__(self, base_model, out_dim):
        super(model_BIDFC, self).__init__()
        self.out_dim = out_dim
        self.backbone = self.get_resnet(base_model)

    def forward(self, x):
        x = self.backbone(x)
        return x

    def get_resnet(self, name, pretrained=False):
        resnets = {"resnet18": torchvision.models.resnet18(pretrained=pretrained, num_classes=self.out_dim),
                   "resnet50": torchvision.models.resnet50(pretrained=pretrained, num_classes=self.out_dim)}
        if name not in resnets.keys():
            raise KeyError(f"{name} is not a valid ResNet version")
        return resnets[name]


if __name__ == '__main__':
    from torchstat import stat
    model1 = model_SimCLR(base_model="resnet18", out_dim=128)
    model2 = model_BIDFC(base_model='resnet18', out_dim=10)
    model3 = model_Pretrian(base_model="resnet18", linear1_out=512, linear2_out=128)
    print(model1)
    print('-'*100)
    print(model2)
    print('-' * 100)
    print(model3)