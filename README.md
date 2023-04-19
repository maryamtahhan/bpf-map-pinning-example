# bpf-map-pinning-example

This repo shows how BPF map pinning can be used by an unprivileged pod in a Kind cluster.

Tested with:

- kind version 0.18.0
- Docker version 23.0.1, build a5ee5b1
- OS: Ubuntu 22.04.2 LTS
- Kernel: 5.15.0-57-generic

The repo contains a Dockerfile which builds a simple docker image called `bpfmap`. This image
contains two examples:

1. A simple example that pins a BPF map.
2. A simple example that accesses a pinned BPF map.

Both examples use the pybpfmap python package available from https://github.com/kot-begemot-uk/pybpfmap.git

To run the kind cluster with the example pods please use the following:

```bash
$  make run-on-kind
$  kubectl create -f pods/pin-pod-spec.yaml
$ kubectl create -f pods/pod-spec.yaml
$ kubectl logs bpfmap-pin-pod
0102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f00
0102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f00
MAP created and pinned
$ kubectl logs bpfmap-pod
MAP retrieved
```

## Kind configuration

The example below shows a kind cluster configuration that takes advantage of the `extraMounts`
parameter to mount host paths: `/tmp/bpf-map/` and `/tmp/bpf-map2/` to the kind worker nodes.
These paths will be used to create a bpffs where a BPF map can be pinned and shared with a non
privileged pod.

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: bpf-map-pinning-deployment # Cluster name

nodes:
- role: control-plane
- role: worker
  extraMounts:
  - hostPath: /tmp/bpf-map/
    containerPath: /tmp/bpf-map/
    propagation: Bidirectional # Propagation needs to be Bidirectional so that the pin pod can pin a map to this bpffs.
    selinuxRelabel: false
- role: worker
  extraMounts:
  - hostPath: /tmp/bpf-map2/
    containerPath: /tmp/bpf-map/
    propagation: Bidirectional
    selinuxRelabel: false
```

The bpffs is created in the Makefile using:

```bash
$ docker exec bpf-map-pinning-deployment-worker mount bpffs /tmp/bpf-map/ -t bpf
$ docker exec bpf-map-pinning-deployment-worker2 mount bpffs /tmp/bpf-map/ -t bpf
```

Kind runs a kernel older than 5.18 - which means in order to access a map CAP_BPF is required unless you run:

```bash
$ docker exec bpf-map-pinning-deployment-worker sysctl kernel.unprivileged_bpf_disabled=0
$ docker exec bpf-map-pinning-deployment-worker2 sysctl kernel.unprivileged_bpf_disabled=0
```

This is also covered in the Makefile when you run `make run-on-kind`

## Pin pod configuration

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: bpfmap-pin-pod                    # Pod name
spec:
  nodeSelector:
    bpfexample: "true"
  containers:
  - name: bpfmap-pin
    image: bpfmap:latest                 # Specify your docker image here, along with PullPolicy and command
    imagePullPolicy: IfNotPresent
    command: ["./tests/pin_bpf_map.py"]
    securityContext:
      capabilities:
        add:
          - BPF                         # CAP_BPF needed to create maps.
    volumeMounts:
      - mountPath: /var/run/example/map/
        name: bpfmap-volume
  volumes:
  - name: bpfmap-volume
    hostPath:
      # directory location on host
      path: /tmp/bpf-map/
      # this field is optional
      type: Directory
  restartPolicy: Never
```

## Unprivileged pod configuration

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: bpfmap-pod                       # Pod name
spec:
  nodeSelector:
    bpfexample: "true"
  containers:
  - name: bpfmap-get
    image: bpfmap:latest                 # Specify your docker image here, along with PullPolicy and command
    imagePullPolicy: IfNotPresent
    command: ["./tests/get_bpf_map.py"]
    volumeMounts:
      - mountPath: /var/run/example/map/
        name: bpfmap-volume
  volumes:
  - name: bpfmap-volume
    hostPath:
      # directory location on host
      path: /tmp/bpf-map/
      # this field is optional
      type: Directory
  restartPolicy: Never
```
