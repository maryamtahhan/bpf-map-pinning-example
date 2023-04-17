#!/bin/bash
mount bpffs /var/run/example/map/ -t bpf
mount --make-shared /var/run/example/map/
