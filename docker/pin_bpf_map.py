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

from pybpfmap.bpfrecord import BPFMap
from pybpfmap.map_types import BPF_MAP_TYPE_HASH

TESTSEQ = "0102030405060708090a0b0c0d0e0f00"
TESTKEY = bytes.fromhex(TESTSEQ)
TESTDATA = bytes.fromhex(TESTSEQ + TESTSEQ + TESTSEQ + TESTSEQ)

def main():
    m = BPFMap(1, BPF_MAP_TYPE_HASH, "test_elem".encode("ascii"), 16, 64, 256, create=True)
    if (m.fd < 0):
        print("Error creating the map")
        sys.exit(0)

    try:
        if os.path.exists("/var/run/example/map/test-map"):
            os.remove("/var/run/example/map/test-map")
    except OSError:
        print("Error deleting previously pinned map")
        sys.exit(0)

    if (not m.pin_map("/var/run/example/map/test-map".encode("ascii"))):
        print("Error pinning the map")
        sys.exit(0)

    m.update_elem(TESTKEY, TESTDATA)
    print(TESTDATA.hex())
    l = m.lookup_elem(TESTKEY)
    print(l.hex())
    m.lookup_elem(TESTKEY)

    print("MAP created and pinned")

if __name__ == "__main__":
    main()
