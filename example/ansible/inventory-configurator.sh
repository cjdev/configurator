#!/bin/bash

# This script demonstrates how you could use configurator as a backend for ansibles dynamic inventories
# See http://www.ansibleworks.com/docs/api.html#external-inventory-scripts for more information

# usage:
# CONFIG=staging ansible-playbook site.yaml -i inventory-configurator.sh
# this will load up ansible and target staging hostgroups

set -e

if [ -v CONFIG ]; then
    declare -x CONFIG=base
else

if [ -v CONFIGURATOR ]; then
    declare -x CONFIGURATOR=http://localhost:5000
else

case "$1" in

    # As of ansible 1.3 there is a single api hook for inventory scripts
    # we must resepond to --list with our configs json
    --list)
        # since there is no other input
        # we must rely on runtime environment for our config name
        curl -sH "Accept: application/json" "${CONFIGURATOR}?config=${CONFIG}"
    ;;

    *)
        # ignore all other api calls
        echo "{}"
    ;;

esac
