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
	kind delete cluster --name bpf-map-pinning-deployment
	rm -rf /tmp/bpf-map/
	rm -rf /tmp/bpf-map2/

.PHONY: setup-kind
setup-kind: del-kind ## Setup a kind cluster called bpf-map-pinning-deployment
	mkdir -p /tmp/bpf-map/
	mkdir -p /tmp/bpf-map2/
	kind create cluster --config kind/kind-config.yaml --name bpf-map-pinning-deployment

.PHONY: kind-deploy
kind-deploy: image ## Deploy the example kind cluster
	@echo "****** Deploy Daemonset  ******"
	@echo
	kind load --name bpf-map-pinning-deployment docker-image bpfmap
	kubectl create -f ./deployments/daemonset-kind.yaml
	@echo
	@echo

.PHONY: run-on-kind
run-on-kind: del-kind setup-kind kind-deploy ## Run the example kind cluster
	@echo "******       Kind Setup complete       ******"
