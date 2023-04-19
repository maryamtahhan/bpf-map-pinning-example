#!/bin/bash
# Copyright(c) Red Hat Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
RUN git pull
RUN git checkout a689da4cce832d867c1b967039556c687244f425
RUN pip3 install -e .
RUN sed -i 's/nosetests3/nosetests/g' Makefile
COPY docker/pin_bpf_map.py /pybpfmap/pybpfmap/tests
RUN chmod +x /pybpfmap/pybpfmap/tests/pin_bpf_map.py
COPY docker/get_bpf_map.py /pybpfmap/pybpfmap/tests
RUN chmod +x /pybpfmap/pybpfmap/tests/get_bpf_map.py
RUN mkdir -p /var/run/example/map/
COPY docker/bpffs.sh /pybpfmap/pybpfmap/
RUN chmod +x /pybpfmap/pybpfmap/bpffs.sh
