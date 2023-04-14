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
	python3-devel

RUN pip3 install "cython>=3.0.0b2"

RUN git clone https://github.com/kot-begemot-uk/pybpfmap.git
WORKDIR pybpfmap/pybpfmap
RUN python3 setup.py build_ext -i
RUN pip install -e .
