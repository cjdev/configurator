#!/bin/sh

set -e

PYINSTALLER_URL='http://downloads.sourceforge.net/project/pyinstaller/2.0/pyinstaller-2.0.tar.bz2'
PYINSTALLER_EXE='dist-utils/pyinstaller-2.0/pyinstaller.py'

if [ -z "${PYTHON_EXE}" ]
then
  PYTHON_EXE=python
fi

if [ ! -f $PYINSTALLER_EXE ]; then
    mkdir -p dist-utils
    curl -Ls $PYINSTALLER_URL | tar -C 'dist-utils' -xj 
fi

$PYTHON_EXE $PYINSTALLER_EXE --onefile configurator.py -o .
