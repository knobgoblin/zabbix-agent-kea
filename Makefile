SHELL  := /bin/bash
RED    := \033[0;31m
GREEN  := \033[0;32m
BLUE   := \033[0;34m
CYAN   := \033[0;36m
YELLOW := \033[1;33m
NC     := \033[0m # No Color
UNAME  := $(shell uname)
PYVERS := $(shell python3 --version | cut -d ' ' -f2)

usage:
	@printf "${YELLOW}make clean                ${GREEN}# Remove all build artefacts.\n"
	@printf "${YELLOW}make test                 ${GREEN}# Execute tests.\n"
	@printf "${YELLOW}make sonarscan            ${GREEN}# Check code quality.\n"
	@printf "${YELLOW}make package              ${GREEN}# Create .deb file.${NC}\n"
	@printf "\n"

export PYTHONPATH := ${CURDIR}/venv/lib/python${PYVERS}/site-packages
export PATH := ${CURDIR}/venv/bin:${PATH}
ifeq ($(UNAME),Darwin)
export SONARSCAN_PATH=/opt/homebrew/bin
else
export SONARSCAN_PATH=/opt/sonar/bin
endif

clean:
	@${CURDIR}/clean.sh

init_virtualenv:
	@python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install -r pip-requirements.txt

use_virtualenv:
	@source venv/bin/activate

package:
	@${CURDIR}/package.sh

test: init_virtualenv use_virtualenv
	@cd tests && ./run_tests.sh

sonarscan: init_virtualenv use_virtualenv test
	@[ -n $${SONARQUBE_TOKEN} ] || (echo "Need a vault for SONARQUBE_TOKEN" && exit 1)
	@[ -n $${SONARQUBE_HOST} ] || (echo "Need a vault for SONARQUBE_HOST" && exit 1)
	@printf "\n"
	@printf "${BLUE}Scanning code using SonarQube ...${NC}\n"
	@printf "\n"
	@${SONARSCAN_PATH}/sonar-scanner -Dsonar.projectKey=zabbix-agent-kea -Dsonar.sources=bin -Dsonar.host.url=${SONARQUBE_HOST} -Dsonar.token=${SONARQUBE_TOKEN} -Dsonar.python.coverage.reportPaths=coverage.xml

.PHONY: package test usage init_virtualenv use_virtualenv clean test sonarscan
.DEFAULT_GOAL := usage
