#!/bin/bash

BUILD_DIR="noise-sources/build"
SOURCE_FILES="../timer.c ../operations.c"
LIB_NAME="jitter2infinitylib"
SO=".so"
DLL=".dll"

GCC="gcc"
MINGW="x86_64-w64-mingw32-gcc"
FLAGS="-shared -fPIC -fno-strict-aliasing -fno-inline"
OPTIMIZATION_LEVELS=("-O0" "-O1" "-O2" "-O3" "-Ofast" "-Og" "-Os")

mkdir -p $BUILD_DIR && cd $BUILD_DIR

for OPT in ${OPTIMIZATION_LEVELS[@]}; do
	LIB_NAME_OPT=${LIB_NAME}${OPT}
	echo Building $LIB_NAME_OPT ...
	$GCC $OPT $FLAGS -o $LIB_NAME_OPT.so $SOURCE_FILES
	$MINGW $OPT $FLAGS -o $LIB_NAME_OPT.dll $SOURCE_FILES
done
