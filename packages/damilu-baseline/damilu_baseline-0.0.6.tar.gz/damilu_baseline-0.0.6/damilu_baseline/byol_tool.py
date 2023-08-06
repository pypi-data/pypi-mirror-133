import torch
from torch import nn
import torchvision.models as models


class BaseSimCLRException(Exception):
    """Base exception"""


class InvalidBackboneError(BaseSimCLRException):
    """Raised when the choice of backbone Convnet is invalid."""


class InvalidDatasetSelection(BaseSimCLRException):
    """Raised when the choice of dataset is invalid."""

class MLPHead(nn.Module):
    def __init__(self, in_channels, mlp_hidden_size, projection_size):
        super(MLPHead, self).__init__()

        self.net = nn.Sequential(
            nn.Linear(in_channels, mlp_hidden_size),
            nn.BatchNorm1d(mlp_hidden_size),
            nn.ReLU(inplace=True),
            nn.Linear(mlp_hidden_size, projection_size)
        )

    def forward(self, x):
        return self.net(x)


class Projector(torch.nn.Module):
    def __init__(self, base_model, linear1_out, linear2_out):
        super(Projector, self).__init__()
        self.resnet_dict = {"resnet18": models.resnet18(pretrained=False, num_classes=128),
                            "resnet50": models.resnet50(pretrained=False, num_classes=128)}

        self.backbone = self._get_basemodel(base_model)
        dim_mlp = self.backbone.fc.in_features

        # add mlp projection head
        self.backbone.fc = nn.Sequential(nn.Linear(dim_mlp, linear1_out),
                                         nn.BatchNorm1d(linear1_out),
                                         nn.ReLU(inplace=True),
                                         nn.Linear(linear1_out, linear2_out)
                                         )

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


if __name__ == '__main__':

    online_network = Projector('resnet18', 512, 128).to('cpu')
    print('online_network:', online_network)