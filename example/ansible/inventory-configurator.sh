#!/bin/bash

# This script demonstrates how you could use configurator as a backend for ansibles dynamic inventories
# See http://www.ansibleworks.com/docs/api.html#external-inventory-scripts for more information

# usage:
# CONFIG=staging ansible-playbook site.yaml -i inventory-configurator.sh
# this will load up ansible and target staging hostgroups

set -e

# assuming we have configurator -d ~/path/to/ansible/host/configs --serve -p 5678
CONFIGURATOR=http://localhost:5678

case "$1" in

    # As of ansible 1.3 there is a single api hook for inventory scripts
    # we must resepond to --list with our configs json
    --list)
        # since there is no other input
        # so we must rely on runtime environment for our config name
        if [ -v CONFIG ]; then
            curl -sH "Accept: application/json" "${CONFIGURATOR}?config=${CONFIG}?node=ansible.inventory"
        else
            curl -sH "Accept: application/json" "${CONFIGURATOR}"
        fi
    ;;

    *)
        # ignore all other api calls
        echo "{}"
    ;;

esac
