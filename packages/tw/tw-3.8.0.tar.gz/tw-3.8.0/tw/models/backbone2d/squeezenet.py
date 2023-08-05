# Copyright 2018 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""SqueezeNet form torchvision.model """
import torch
import torch.nn as nn
import torch.nn.init as init
from tw.utils.checkpoint import load_state_dict_from_url

model_urls = {
    'squeezenet1_0': 'https://download.pytorch.org/models/squeezenet1_0-a815701f.pth',
    'squeezenet1_1': 'https://download.pytorch.org/models/squeezenet1_1-f364aa15.pth',
}


class Fire(nn.Module):
  def __init__(self, inplanes, squeeze_planes,
               expand1x1_planes, expand3x3_planes):
    super(Fire, self).__init__()
    self.inplanes = inplanes
    self.squeeze = nn.Conv2d(inplanes, squeeze_planes, kernel_size=1)
    self.squeeze_activation = nn.ReLU(inplace=True)
    self.expand1x1 = nn.Conv2d(squeeze_planes, expand1x1_planes,
                               kernel_size=1)
    self.expand1x1_activation = nn.ReLU(inplace=True)
    self.expand3x3 = nn.Conv2d(squeeze_planes, expand3x3_planes,
                               kernel_size=3, padding=1)
    self.expand3x3_activation = nn.ReLU(inplace=True)

  def forward(self, x):
    x = self.squeeze_activation(self.squeeze(x))
    return torch.cat([
        self.expand1x1_activation(self.expand1x1(x)),
        self.expand3x3_activation(self.expand3x3(x))
    ], 1)


class SqueezeNet(nn.Module):

  MEAN = [0.485, 0.456, 0.406]
  STD = [0.229, 0.224, 0.225]
  SIZE = [224, 224]
  SCALE = 255
  CROP = 0.875

  def __init__(self, version='1_0', num_classes=1000):
    super(SqueezeNet, self).__init__()
    self.num_classes = num_classes
    if version == '1_0':
      self.features = nn.Sequential(
          nn.Conv2d(3, 96, kernel_size=7, stride=2),
          nn.ReLU(inplace=True),
          nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
          Fire(96, 16, 64, 64),
          Fire(128, 16, 64, 64),
          Fire(128, 32, 128, 128),
          nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
          Fire(256, 32, 128, 128),
          Fire(256, 48, 192, 192),
          Fire(384, 48, 192, 192),
          Fire(384, 64, 256, 256),
          nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
          Fire(512, 64, 256, 256),
      )
    elif version == '1_1':
      self.features = nn.Sequential(
          nn.Conv2d(3, 64, kernel_size=3, stride=2),
          nn.ReLU(inplace=True),
          nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
          Fire(64, 16, 64, 64),
          Fire(128, 16, 64, 64),
          nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
          Fire(128, 32, 128, 128),
          Fire(256, 32, 128, 128),
          nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
          Fire(256, 48, 192, 192),
          Fire(384, 48, 192, 192),
          Fire(384, 64, 256, 256),
          Fire(512, 64, 256, 256),
      )
    else:
      # FIXME: Is this needed? SqueezeNet should only be called from the
      # FIXME: squeezenet1_x() functions
      # FIXME: This checking is not done for the other models
      raise ValueError("Unsupported SqueezeNet version {version}:"
                       "1_0 or 1_1 expected".format(version=version))

    # Final convolution is initialized differently from the rest
    final_conv = nn.Conv2d(512, self.num_classes, kernel_size=1)
    self.classifier = nn.Sequential(
        nn.Dropout(p=0.5),
        final_conv,
        nn.ReLU(inplace=True),
        nn.AdaptiveAvgPool2d((1, 1))
    )

    for m in self.modules():
      if isinstance(m, nn.Conv2d):
        if m is final_conv:
          init.normal_(m.weight, mean=0.0, std=0.01)
        else:
          init.kaiming_uniform_(m.weight)
        if m.bias is not None:
          init.constant_(m.bias, 0)

  def forward(self, x):
    x = self.features(x)
    x = self.classifier(x)
    return x.view(x.size(0), -1)


def _squeezenet(version, pretrained, **kwargs):
  model = SqueezeNet(version, **kwargs)
  if pretrained:
    arch = 'squeezenet' + version
    load_state_dict_from_url(model, model_urls[arch])
  return model


def squeezenet1_0(pretrained=False, **kwargs):
  r"""SqueezeNet model architecture from the `"SqueezeNet: AlexNet-level
  accuracy with 50x fewer parameters and <0.5MB model size"
  <https://arxiv.org/abs/1602.07360>`_ paper.

  Args:
      pretrained (bool): If True, returns a model pre-trained on ImageNet
      progress (bool): If True, displays a progress bar of the download to stderr
  """
  return _squeezenet('1_0', pretrained, **kwargs)


def squeezenet1_1(pretrained=False, **kwargs):
  r"""SqueezeNet 1.1 model from the `official SqueezeNet repo
  <https://github.com/DeepScale/SqueezeNet/tree/master/SqueezeNet_v1.1>`_.
  SqueezeNet 1.1 has 2.4x less computation and slightly fewer parameters
  than SqueezeNet 1.0, without sacrificing accuracy.

  Args:
      pretrained (bool): If True, returns a model pre-trained on ImageNet
      progress (bool): If True, displays a progress bar of the download to stderr
  """
  return _squeezenet('1_1', pretrained, **kwargs)
