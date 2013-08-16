#!/bin/sh

set -e

PKG_DIR="configurator-$(uname -srm | tr ' ' '-')"
DIST_DIR=./dist
DIST=${DIST_DIR}/configurator

mkdir -p ${DIST_DIR}/${PKG_DIR}

cp ${DIST} ${DIST_DIR}/${PKG_DIR}

tar -czf ${DIST_DIR}/${PKG_DIR}.tar.gz -C ${DIST_DIR} ${PKG_DIR}

