#!/usr/bin/env bash

PYTHON_ARCHIVE="Python-3.10-macOS-support.b6.tar.gz"
PYTHON_URL="https://github.com/beeware/Python-Apple-support/releases/download/3.10-b6/${PYTHON_ARCHIVE}"
SUPPORT="test-xcode/Demo/Support"

cd ${SUPPORT}
wget ${PYTHON_URL} 
tar xvf ${PYTHON_ARCHIVE}
rm -f ${PYTHON_ARCHIVE}
