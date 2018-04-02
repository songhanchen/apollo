#!/usr/bin/env python

###############################################################################
# Copyright 2018 The Apollo Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

import os
import sys
import argparse
import glob
import math
import numpy as np

import matplotlib.pyplot as plt


def select(pose):
    idx = np.ones_like(pose[:, 0])
    for i in xrange(pose.shape[0]):
        if pose[i, 1] > 0.1:
            idx[i] = 0
    return idx == 1

def show_v_kappa_plot(pose):
    idx = select(pose)
    plt.plot(pose[idx, 3], pose[idx, 0], 'o')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Generate future trajectory based on localization")
    parser.add_argument('path', type = str, help = 'rosbag file or directory')

    args = parser.parse_args()
    path = args.path

    if not os.path.exists(path):
        logging.error("Fail to find path: {}".format(path))
        os._exists(-1)
    if os.path.isdir(path):
        pass
    if os.path.isfile(path):
        pose = np.genfromtxt(path, delimiter=',')
        show_v_kappa_plot(pose)
        