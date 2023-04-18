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

.PHONY: help all
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

all: image

##@ General Build - assumes K8s environment is already setup
image: ## Build docker image
	@echo "******  docker Image    ******"
	@echo
	docker build -t bpfmap -f docker/Dockerfile .
	@echo
	@echo

.PHONY: del-kind
del-kind: ## Remove a kind cluster called bpf-map-pinning-deployment
ifeq ($(docker ps -a | grep bpf-map-pinning-deployment-worker | wc -l ), 1)
	docker exec bpf-map-pinning-deployment-worker umount /tmp/bpf-map/
else ifeq ($( docker ps -a | grep bpf-map-pinning-deployment-worker2 | wc -l ), 1)
	docker exec bpf-map-pinning-deployment-worker umount /tmp/bpf-map/
endif
	kind delete cluster --name bpf-map-pinning-deployment
	rm -rf /tmp/bpf-map/
	rm -rf /tmp/bpf-map2/

.PHONY: setup-kind
setup-kind: del-kind ## Setup a kind cluster called bpf-map-pinning-deployment
	mkdir -p /tmp/bpf-map/
	mkdir -p /tmp/bpf-map2/
	kind create cluster --config kind/kind-config.yaml

.PHONY: kind-deploy
kind-load: image ## Load the image in the kind cluster
	@echo "****** Load bpfmap image  ******"
	@echo
	kind load --name bpf-map-pinning-deployment docker-image bpfmap
	@echo
	@echo

.PHONY: label-kind-node
label-kind-node: ## label the kind worker nodes with bpfexample="true"
	kubectl label node bpf-map-pinning-deployment-worker bpfexample=true

.PHONY: run-on-kind
run-on-kind: del-kind image setup-kind kind-load label-kind-node ## Run the example kind cluster
	docker exec bpf-map-pinning-deployment-worker mount bpffs /tmp/bpf-map/ -t bpf
	docker exec bpf-map-pinning-deployment-worker2 mount bpffs /tmp/bpf-map/ -t bpf
	docker exec bpf-map-pinning-deployment-worker sysctl kernel.unprivileged_bpf_disabled=0
	docker exec bpf-map-pinning-deployment-worker2 sysctl kernel.unprivileged_bpf_disabled=0
	@echo "******       Kind Setup complete       ******"
