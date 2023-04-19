#!/usr/bin/python3
# Copyright 2023 (c) RedHat Inc
# Copyright 2023 (c) Cambridge Greys Ltd
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided
# that the following conditions are met:
# 1. Redistributions of source code must retain the above
#    copyright notice, this list of conditions and the
#    following disclaimer.
# 2. Redistributions in binary form must reproduce the
#    above copyright notice, this list of conditions and
#    the following disclaimer in the documentation and/or
#    other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names
#    of its contributors may be used to endorse or promote
#    products derived from this software without specific
#    prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
