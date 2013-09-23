#!/bin/bash

# Ansible can take vars at runtime as -e or --extra-vars

# Here, we use configurator and some simple shell scripting
# to provide dynamic configuration to ansible playbooks

CONFIGURATOR=http://localhost:5678

if [ $# -eq 0 ]; then
    echo "./playbook-configurator.sh <config> [ansible opts...]"
    exit 1
else
    # grab the first arg as the config name
    declare -x CONFIG=$1
    shift

    # forward the rest of the args to ansible,
    # plus the configurator vars fetched over http
    ansible-playbook -e configurator_vars=<(curl "${CONFIGURATOR}?config=${CONFIG}") $@
fi
