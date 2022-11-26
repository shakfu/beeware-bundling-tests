#!/usr/bin/env bash

SUPPORT="test-xcode/Demo/Support"
SUBPROJECTS="test-cmake test-cmake-objc"

rm -rf ${SUPPORT}/Python-3.10-macOS-support.*
rm -rf ${SUPPORT}/python-stdlib
rm -rf ${SUPPORT}/Python.xcframework
rm -rf ${SUPPORT}/VERSIONS

for target in ${SUBPROJECTS}
do
	echo "cleaning: ${target}"
	rm -rf ${target}/build
done
