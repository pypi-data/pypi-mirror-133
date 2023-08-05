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
r"""https://github.com/fyu/drn
"""
import math
import torch.nn as nn
import tw

BatchNorm = nn.SyncBatchNorm


model_urls = {
    'resnet50': 'https://download.pytorch.org/models/resnet50-19c8e357.pth',
    'drn-c-26': 'http://dl.yf.io/drn/drn_c_26-ddedf421.pth',
    'drn-c-42': 'http://dl.yf.io/drn/drn_c_42-9d336e8c.pth',
    'drn-c-58': 'http://dl.yf.io/drn/drn_c_58-0a53a92c.pth',
    'drn-d-22': 'http://dl.yf.io/drn/drn_d_22-4bd2f8ea.pth',
    'drn-d-38': 'http://dl.yf.io/drn/drn_d_38-eebb45f0.pth',
    'drn-d-54': 'http://dl.yf.io/drn/drn_d_54-0e0534ff.pth',
    'drn-d-105': 'http://dl.yf.io/drn/drn_d_105-12b40979.pth'
}


def conv3x3(in_planes, out_planes, stride=1, padding=1, dilation=1):
  return nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride,
                   padding=padding, bias=False, dilation=dilation)


class BasicBlock(nn.Module):
  expansion = 1

  def __init__(self, inplanes, planes, stride=1, downsample=None,
               dilation=(1, 1), residual=True):
    super(BasicBlock, self).__init__()
    self.conv1 = conv3x3(inplanes, planes, stride,
                         padding=dilation[0], dilation=dilation[0])
    self.bn1 = BatchNorm(planes)
    self.relu = nn.ReLU(inplace=True)
    self.conv2 = conv3x3(planes, planes,
                         padding=dilation[1], dilation=dilation[1])
    self.bn2 = BatchNorm(planes)
    self.downsample = downsample
    self.stride = stride
    self.residual = residual

  def forward(self, x):
    residual = x

    out = self.conv1(x)
    out = self.bn1(out)
    out = self.relu(out)

    out = self.conv2(out)
    out = self.bn2(out)

    if self.downsample is not None:
      residual = self.downsample(x)
    if self.residual:
      out += residual
    out = self.relu(out)

    return out


class Bottleneck(nn.Module):
  expansion = 4

  def __init__(self, inplanes, planes, stride=1, downsample=None,
               dilation=(1, 1), residual=True):
    super(Bottleneck, self).__init__()
    self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=1, bias=False)
    self.bn1 = BatchNorm(planes)
    self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride,
                           padding=dilation[1], bias=False,
                           dilation=dilation[1])
    self.bn2 = BatchNorm(planes)
    self.conv3 = nn.Conv2d(planes, planes * 4, kernel_size=1, bias=False)
    self.bn3 = BatchNorm(planes * 4)
    self.relu = nn.ReLU(inplace=True)
    self.downsample = downsample
    self.stride = stride

  def forward(self, x):
    residual = x

    out = self.conv1(x)
    out = self.bn1(out)
    out = self.relu(out)

    out = self.conv2(out)
    out = self.bn2(out)
    out = self.relu(out)

    out = self.conv3(out)
    out = self.bn3(out)

    if self.downsample is not None:
      residual = self.downsample(x)

    out += residual
    out = self.relu(out)

    return out


class DRN(nn.Module):

  MEAN = [0.485, 0.456, 0.406]
  STD = [0.229, 0.224, 0.225]
  SIZE = [224, 224]
  SCALE = 255
  CROP = 0.875

  def __init__(self, block, layers, arch='D', channels=(16, 32, 64, 128, 256, 512, 512, 512)):
    super(DRN, self).__init__()
    self.inplanes = channels[0]
    self.out_dim = channels[-1]
    self.arch = arch

    if arch == 'C':
      self.conv1 = nn.Conv2d(3, channels[0], kernel_size=7, stride=1, padding=3, bias=False)
      self.bn1 = BatchNorm(channels[0])
      self.relu = nn.ReLU(inplace=True)

      self.layer1 = self._make_layer(
          BasicBlock, channels[0], layers[0], stride=1)
      self.layer2 = self._make_layer(
          BasicBlock, channels[1], layers[1], stride=2)

    elif arch == 'D':
      self.layer0 = nn.Sequential(
          nn.Conv2d(3, channels[0], kernel_size=7, stride=1, padding=3, bias=False),
          BatchNorm(channels[0]),
          nn.ReLU(inplace=True)
      )

      self.layer1 = self._make_conv_layers(channels[0], layers[0], stride=1)
      self.layer2 = self._make_conv_layers(channels[1], layers[1], stride=2)

    self.layer3 = self._make_layer(block, channels[2], layers[2], stride=2)
    self.layer4 = self._make_layer(block, channels[3], layers[3], stride=2)
    self.layer5 = self._make_layer(block, channels[4], layers[4], dilation=2, new_level=False)
    self.layer6 = None if layers[5] == 0 else self._make_layer(
        block, channels[5], layers[5], dilation=4, new_level=False)

    if arch == 'C':
      self.layer7 = None if layers[6] == 0 else \
          self._make_layer(BasicBlock, channels[6], layers[6], dilation=2, new_level=False, residual=False)
      self.layer8 = None if layers[7] == 0 else \
          self._make_layer(BasicBlock, channels[7], layers[7], dilation=1, new_level=False, residual=False)
    elif arch == 'D':
      self.layer7 = None if layers[6] == 0 else self._make_conv_layers(channels[6], layers[6], dilation=2)
      self.layer8 = None if layers[7] == 0 else self._make_conv_layers(channels[7], layers[7], dilation=1)

    self._init_weight()

  def _init_weight(self):
    for m in self.modules():
      if isinstance(m, nn.Conv2d):
        n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
        m.weight.data.normal_(0, math.sqrt(2. / n))
      elif isinstance(m, BatchNorm):
        m.weight.data.fill_(1)
        m.bias.data.zero_()
      elif isinstance(m, nn.BatchNorm2d):
        m.weight.data.fill_(1)
        m.bias.data.zero_()

  def _make_layer(self, block, planes, blocks, stride=1, dilation=1,
                  new_level=True, residual=True):
    assert dilation == 1 or dilation % 2 == 0
    downsample = None
    if stride != 1 or self.inplanes != planes * block.expansion:
      downsample = nn.Sequential(
          nn.Conv2d(self.inplanes, planes * block.expansion,
                    kernel_size=1, stride=stride, bias=False),
          BatchNorm(planes * block.expansion))

    layers = list()
    layers.append(block(
        self.inplanes, planes, stride, downsample,
        dilation=(1, 1) if dilation == 1 else (
            dilation // 2 if new_level else dilation, dilation),
        residual=residual))
    self.inplanes = planes * block.expansion
    for i in range(1, blocks):
      layers.append(block(self.inplanes, planes, residual=residual,
                          dilation=(dilation, dilation)))

    return nn.Sequential(*layers)

  def _make_conv_layers(self, channels, convs, stride=1, dilation=1):
    modules = []
    for i in range(convs):
      modules.extend([
          nn.Conv2d(self.inplanes, channels, kernel_size=3,
                    stride=stride if i == 0 else 1,
                    padding=dilation, bias=False, dilation=dilation),
          BatchNorm(channels),
          nn.ReLU(inplace=True)])
      self.inplanes = channels
    return nn.Sequential(*modules)

  def forward(self, x):
    if self.arch == 'C':
      x = self.conv1(x)
      x = self.bn1(x)
      x = self.relu(x)
    elif self.arch == 'D':
      x = self.layer0(x)

    x = self.layer1(x)
    x = self.layer2(x)

    x = self.layer3(x)
    low_level_feat = x

    x = self.layer4(x)
    x = self.layer5(x)

    if self.layer6 is not None:
      x = self.layer6(x)

    if self.layer7 is not None:
      x = self.layer7(x)

    if self.layer8 is not None:
      x = self.layer8(x)

    return x  # , low_level_feat


class DRN_A(nn.Module):
  def __init__(self, block, layers):
    self.inplanes = 64
    super(DRN_A, self).__init__()
    self.out_dim = 512 * block.expansion
    self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3,
                           bias=False)
    self.bn1 = BatchNorm(64)
    self.relu = nn.ReLU(inplace=True)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    self.layer1 = self._make_layer(block, 64, layers[0])
    self.layer2 = self._make_layer(
        block, 128, layers[1], stride=2)
    self.layer3 = self._make_layer(block, 256, layers[2], stride=1,
                                   dilation=2)
    self.layer4 = self._make_layer(block, 512, layers[3], stride=1,
                                   dilation=4)

    self._init_weight()

  def _init_weight(self):
    for m in self.modules():
      if isinstance(m, nn.Conv2d):
        n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
        m.weight.data.normal_(0, math.sqrt(2. / n))
      elif isinstance(m, BatchNorm):
        m.weight.data.fill_(1)
        m.bias.data.zero_()
      elif isinstance(m, nn.BatchNorm2d):
        m.weight.data.fill_(1)
        m.bias.data.zero_()

  def _make_layer(self, block, planes, blocks, stride=1, dilation=1):
    downsample = None
    if stride != 1 or self.inplanes != planes * block.expansion:
      downsample = nn.Sequential(
          nn.Conv2d(self.inplanes, planes * block.expansion,
                    kernel_size=1, stride=stride, bias=False),
          BatchNorm(planes * block.expansion),
      )

    layers = []
    layers.append(block(self.inplanes, planes, stride,
                        downsample))
    self.inplanes = planes * block.expansion
    for i in range(1, blocks):
      layers.append(block(self.inplanes, planes,
                          dilation=(dilation, dilation, )))

    return nn.Sequential(*layers)

  def forward(self, x):
    x = self.conv1(x)
    x = self.bn1(x)
    x = self.relu(x)
    x = self.maxpool(x)

    x = self.layer1(x)
    x = self.layer2(x)
    x = self.layer3(x)
    x = self.layer4(x)

    return x


def drn_a_50(pretrained=False, **kwargs):
  model = DRN_A(Bottleneck, [3, 4, 6, 3])
  if pretrained:
    tw.checkpoint.load_state_dict_from_url(model, model_urls['drn-a-50'])
  return model


def drn_c_26(pretrained=False, **kwargs):
  model = DRN(BasicBlock, [1, 1, 2, 2, 2, 2, 1, 1], arch='C')
  if pretrained:
    tw.checkpoint.load_state_dict_from_url(model, model_urls['drn-c-26'])
  return model


def drn_c_42(pretrained=False, **kwargs):
  model = DRN(BasicBlock, [1, 1, 3, 4, 6, 3, 1, 1], arch='C')
  if pretrained:
    tw.checkpoint.load_state_dict_from_url(model, model_urls['drn-c-42'])
  return model


def drn_c_58(pretrained=False, **kwargs):
  model = DRN(Bottleneck, [1, 1, 3, 4, 6, 3, 1, 1], arch='C')
  if pretrained:
    tw.checkpoint.load_state_dict_from_url(model, model_urls['drn-c-58'])
  return model


def drn_d_22(pretrained=False, **kwargs):
  model = DRN(BasicBlock, [1, 1, 2, 2, 2, 2, 1, 1], arch='D')
  if pretrained:
    tw.checkpoint.load_state_dict_from_url(model, model_urls['drn-d-22'])
  return model


def drn_d_24(pretrained=False, **kwargs):
  model = DRN(BasicBlock, [1, 1, 2, 2, 2, 2, 2, 2], arch='D')
  if pretrained:
    tw.checkpoint.load_state_dict_from_url(model, model_urls['drn-d-24'])
  return model


def drn_d_38(pretrained=False, **kwargs):
  model = DRN(BasicBlock, [1, 1, 3, 4, 6, 3, 1, 1], arch='D')
  if pretrained:
    tw.checkpoint.load_state_dict_from_url(model, model_urls['drn-d-38'])
  return model


def drn_d_40(pretrained=False, **kwargs):
  model = DRN(BasicBlock, [1, 1, 3, 4, 6, 3, 2, 2], arch='D')
  if pretrained:
    tw.checkpoint.load_state_dict_from_url(model, model_urls['drn-d-40'])
  return model


def drn_d_54(pretrained=False, **kwargs):
  model = DRN(Bottleneck, [1, 1, 3, 4, 6, 3, 1, 1], arch='D')
  if pretrained:
    tw.checkpoint.load_state_dict_from_url(model, model_urls['drn-d-54'])
  return model


def drn_d_105(pretrained=False, **kwargs):
  model = DRN(Bottleneck, [1, 1, 3, 4, 23, 3, 1, 1], arch='D')
  if pretrained:
    tw.checkpoint.load_state_dict_from_url(model, model_urls['drn-d-105'])
  return model


if __name__ == "__main__":
  import torch
  model = drn_a_50()
  input = torch.rand(1, 3, 512, 512)
  output, low_level_feat = model(input)
  print(output.size())
  print(low_level_feat.size())
