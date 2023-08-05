# Copyright 2021 The KaiJIN Authors. All Rights Reserved.
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

import time
import numpy as np
import cv2
import torch
from torchvision import transforms
from .nets import DSFDNet
from .box_utils import nms_
import os

img_mean = np.array([104., 117., 123.])[:, np.newaxis, np.newaxis].astype('float32')


class DSFD():

  def __init__(self, device='cuda:0', pretrain='_checkpoints/detection/face_detector/dsfd_vgg_0.880.pth'):

    tstamp = time.time()
    self.device = device

    print('[DSFD] loading with', self.device)
    self.net = DSFDNet(device=self.device).to(self.device)
    state_dict = torch.load(pretrain, map_location=self.device)
    self.net.load_state_dict(state_dict)
    self.net.eval()
    print('[DSFD] finished loading (%.4f sec)' % (time.time() - tstamp))

  def detect_faces(self, image, conf_th=0.8, scales=[1]):

    w, h = image.shape[1], image.shape[0]

    bboxes = np.empty(shape=(0, 5))

    with torch.no_grad():
      for s in scales:
        scaled_img = cv2.resize(image, dsize=(0, 0), fx=s, fy=s, interpolation=cv2.INTER_LINEAR)

        scaled_img = np.swapaxes(scaled_img, 1, 2)
        scaled_img = np.swapaxes(scaled_img, 1, 0)
        scaled_img = scaled_img[[2, 1, 0], :, :]
        scaled_img = scaled_img.astype('float32')
        scaled_img -= img_mean
        scaled_img = scaled_img[[2, 1, 0], :, :]
        x = torch.from_numpy(scaled_img).unsqueeze(0).to(self.device)
        y = self.net(x)

        detections = y.data
        scale = torch.Tensor([w, h, w, h])

        for i in range(detections.size(1)):
          j = 0
          while detections[0, i, j, 0] > conf_th:
            score = detections[0, i, j, 0]
            pt = (detections[0, i, j, 1:] * scale).cpu().numpy()
            bbox = (pt[0], pt[1], pt[2], pt[3], score)
            bboxes = np.vstack((bboxes, bbox))
            j += 1

      keep = nms_(bboxes, 0.1)
      bboxes = bboxes[keep]

    return bboxes
