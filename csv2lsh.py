#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#
# Copyright 2014 Robert Bird
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# csv2lsh.py
# Version 0.1
# A simple program for converting CSV lines to locality sensitive hashes
# or a stream of unicode characters suitable for use in blar.py or
# archive. Recommend bzip2 for compression of both outputs


from sys import stdin, stdout
import argparse
import numpy as np
import array


def locality_hash_vector(v, width):
    return "".join(['1' if np.dot(PROJECTION_VECTORS[x], v) > 0 else '0' for x in xrange(width)])


def generate_random_projections(t, l, w):
    pv = []
    if t=='hypercube':
        for vector in xrange(w):
            np.random.seed(vector)
            v = np.random.randint(2, size=l)
            counter = 0
            for e in v:
                if e == 0:
                    v[counter] = -0x1
                    counter += 0x1
                else:
                    v[counter] = 0x1
                    counter += 0x1
            pv.append(v)
    else:
        for vector in xrange(w):
            np.random.seed(vector)
            pv.append(normalize(np.random.randn(0x1, l)))
    return pv


parser = argparse.ArgumentParser()

parser.add_argument(
    '-w',
    action='store',
    dest='width',
    default=32,
    type=int,
    help='Set the width in bits of the LSH; default=32',
    )

parser.add_argument(
    '-t',
    action='store',
    dest='type',
    default='hypercube',
    type=str,
    help='Set the LSH type: hypercube, normal; default=hypercube',
    )

parser.add_argument(
    '-g',
    action='store_true',
    dest='genome',
    default=False,
    help='Generate a blar.py genomic output, width must be <=8; default=OFF',
    )

args = vars(parser.parse_args())

width = args['width']
genome = args['genome']
not_first = False

if genome:
    if width >= 8:
        width = 8
        pad = ""
    if width < 8:
        pad = "".join(['0']*(8-width))
    for line in stdin:
        if not_first == True:
            out = locality_hash_vector([float(x) for x in line.split(',')], width)
            out = "".join([out,pad])
            out = unichr(int(out, 2))
            stdout.write(out.encode('utf-8'))
        else:
            length = len(line.split(','))
            not_first = True
            PROJECTION_VECTORS = generate_random_projections(args['type'], length, width)
            out = locality_hash_vector([float(x) for x in line.split(',')], width)
            out = "".join([out,pad])
            out = unichr(int(out, 2))
            stdout.write(out.encode('utf-8'))
else:
    for line in stdin:
        if not_first == True:
            print locality_hash_vector([float(x) for x in line.split(',')], width)
        else:
            length = len(line.split(','))
            not_first = True
            PROJECTION_VECTORS = generate_random_projections(args['type'], length, width)
            print locality_hash_vector([float(x) for x in line.split(',')], width)