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
import rosbag
import genpy
import glob
import math
from std_msgs.msg import String
import numpy as np

import common.proto_utils as proto_utils
from modules.localization.proto.localization_pb2 import LocalizationEstimate

import logging
logging.basicConfig(level=logging.DEBUG)


def hypot(x, y, z):
    return np.sqrt(x * x + y * y + z * z)


def get_pose_list(rosbag_in):
    # iteration to generate total trajectory
    pose_list = []
    with rosbag.Bag(rosbag_in, 'r') as bag_in:
        for topic, localization, t in bag_in.read_messages():
            if topic != '/apollo/localization/pose':
                continue
            if localization.pose == None:
                print "No pose, skip"
                continue
            pose = localization.pose
            if pose.linear_velocity == None or \
               pose.linear_acceleration == None or \
               pose.angular_velocity == None or \
               pose.heading == None:
                print "No v, a or w, skip"
                continue
            v = hypot(pose.linear_velocity.x,
                      pose.linear_velocity.y,
                      pose.linear_velocity.z)
            w = hypot(pose.angular_velocity.x,
                      pose.angular_velocity.y,
                      pose.angular_velocity.z)
            a = pose.linear_acceleration.x * np.cos(pose.heading) + \
                pose.linear_acceleration.y * np.sin(pose.heading)
            # if a > 0.5:
            #     print "posivite acc [", a, "]"
            #     continue
            if v < 2.0:
                print "Too small v [", v, "] skip"
                continue
            kappa = abs(w / v)
            if kappa < 0.02:
            	print "Too small kappa [", kappa, "] skip"
            	continue
            centripetal_acc = v * v * kappa
            pose_list.append([v, a, w, kappa, centripetal_acc])
            print(v, w, kappa, centripetal_acc)
    return pose_list


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
        bag_files = glob.glob(path + '/*.bag')
        print "Length of files:", len(bag_files)
        for i, bag_file in enumerate(bag_files):
            print "Process File", i, ":", bag_file
            bag_name = os.path.splitext(os.path.basename(bag_file))[0]
            pose_np = get_pose_list(bag_file)
            path_out = os.path.dirname(bag_file) + '/' + bag_name + \
                  '_pose.csv'
            np.savetxt(path_out, pose_np, delimiter=",")
            print "save data into", path_out
            
    if os.path.isfile(path):
        bag_name = os.path.splitext(os.path.basename(path))[0]
        print "Get started"
        pose_list = get_pose_list(path)
        print "pose number = ", len(pose_list)
        pose_np = np.array(pose_list)
        print "pose_np shape = ", pose_np.shape
        path_out = os.path.dirname(path) + '/' + bag_name + \
                  '_pose.csv'
        np.savetxt(path_out, pose_np, delimiter=",")
        print "save data into", path_out
