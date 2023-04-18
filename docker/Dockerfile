# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) Red Hat Inc.

FROM amd64/alpine:3.17

# Setup container to build CNDP applications
RUN apk --no-cache -U add gcc \
    libbpf \
	libbpf-dev \
	py3-pip \
	git \
	python3-dev \
	libc-dev \
	linux-headers

env PYTHONPATH /pybpfmap:$PYTHONPATH

RUN pip3 install "cython>=3.0.0b2"
RUN pip3 install nose3
RUN git clone https://github.com/kot-begemot-uk/pybpfmap.git
WORKDIR pybpfmap/pybpfmap
RUN git checkout fc6db0c
#RUN python3 setup.py build_ext -i
RUN pip3 install -e .
RUN sed -i 's/nosetests3/nosetests/g' Makefile
COPY docker/pin_bpf_map.py /pybpfmap/pybpfmap/tests
RUN chmod +x /pybpfmap/pybpfmap/tests/pin_bpf_map.py
COPY docker/get_bpf_map.py /pybpfmap/pybpfmap/tests
RUN chmod +x /pybpfmap/pybpfmap/tests/get_bpf_map.py
RUN mkdir -p /var/run/example/map/
COPY docker/bpffs.sh /pybpfmap/pybpfmap/
RUN chmod +x /pybpfmap/pybpfmap/bpffs.sh
# On startup run the bpffs.sh script then run ./tests/pin_bpf_map.py
#
