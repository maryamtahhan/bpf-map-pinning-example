# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) Red Hat Inc.

FROM fedora:37 AS build

# Setup container to build CNDP applications
RUN dnf -y upgrade && dnf -y install \
    @development-tools \
    libbpf-devel \
    libbpf \
	bpftool \
	python3-pip \
	git \
	python-devel \
	python3-devel \
	python3-nose

env PYTHONPATH /pybpfmap/:$PYTHONPATH

RUN pip3 install "cython>=3.0.0b2"
RUN pip3 install nose3
RUN git clone https://github.com/kot-begemot-uk/pybpfmap.git
WORKDIR pybpfmap/pybpfmap
RUN git checkout fc6db0c
RUN python3 setup.py build_ext -i
RUN pip3 install -e .
RUN sed -i 's/nosetests3/nosetests-3/g' Makefile
COPY docker/pin_bpf_map.py /pybpfmap/pybpfmap/tests
RUN chmod +x /pybpfmap/pybpfmap/tests/pin_bpf_map.py
RUN mkdir -p /var/run/example/map/
COPY docker/bpffs.sh /pybpfmap/pybpfmap/
RUN chmod +x /pybpfmap/pybpfmap/bpffs.sh
# On startup run the bpffs.sh script then run ./tests/pin_bpf_map.py
#
