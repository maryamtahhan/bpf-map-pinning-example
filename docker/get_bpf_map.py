#!/usr/bin/python3


'''BPF Map functional test
'''

# pybpfmap, Copyright (c) 2023 RedHat Inc
# pybpfmap, Copyright (c) 2023 Cambridge Greys Ltd

# This source code is licensed under both the BSD-style license (found in the
# LICENSE file in the root directory of this source tree) and the GPLv2 (found
# in the COPYING file in the root directory of this source tree).
# You may select, at your option, one of the above-listed licenses.

import sys
import os

from pybpfmap.bpfrecord import PinnedBPFMap

def main():
    m = PinnedBPFMap("/var/run/example/map/test-map")
    if (m.fd < 0):
        print("Error retrieving the map")
        sys.exit(0)
    print("MAP retrieved")

if __name__ == "__main__":
    main()
