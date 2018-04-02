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
import glob
import argparse
import datetime

import numpy as np

def load_csv(filename):
    """
    load training samples from *.hdf5 file
    """
    if not(os.path.exists(filename)):
        print "file:", filename, "does not exist"
        os._exit(1)
    if os.path.splitext(filename)[1] != '.csv':
        print "file:", filename, "is not a csv file"
        os._exit(1)

    values = np.genfromtxt(filename, delimiter=',')
    print "load data size:", values.shape[0]
    if values.shape[0] == 0:
        return None
    return values


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'generate training samples\
            from a specified directory')
    parser.add_argument('directory', type=str,
            help='directory contains feature files')
    args = parser.parse_args()
    path = args.directory

    print "load csv from directory:", format(path)
    if os.path.isdir(path):
        features = None

        csv_files = glob.glob(path + '/*.csv')
        print "Length of files:", len(csv_files)
        for i, csv_file in enumerate(csv_files):
            print "Process File", i, ":", csv_file
            feature = load_csv(csv_file)
            if feature is None:
                continue
            features = np.concatenate((features, feature), axis=0) if features is not None \
                    else feature
    else:
        print "Fail to find", path
        os._exit(-1)

    date = datetime.datetime.now().strftime('%Y-%m-%d')
    sample_dir = path
    if not os.path.exists(sample_dir):
        os.makedirs(sample_dir)
    sample_file = sample_dir + '/csv_' + date + '.csv'
    np.savetxt(sample_file, features, delimiter=",")
    print "Save samples file to:", sample_file

