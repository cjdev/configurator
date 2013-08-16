#!/bin/sh

set -e

if [ -n $1 ]
then
  VERSION="-${1}"
fi

PKG_DIR="configurator${VERSION}-$(uname -srm | tr ' ' '-')"
DIST_DIR=./dist
DIST=${DIST_DIR}/configurator

mkdir -p ${DIST_DIR}/${PKG_DIR}

cp ${DIST} ${DIST_DIR}/${PKG_DIR}
cp LICENSE ${DIST_DIR}/${PKG_DIR}

tar -czf ${DIST_DIR}/${PKG_DIR}.tar.gz -C ${DIST_DIR} ${PKG_DIR}

