#!/bin/bash

mkdir -p noise-sources/build && cd $_

gcc -O0 -shared -o jitter2infinitylib.so -fPIC ../timer.c ../operations.c
x86_64-w64-mingw32-gcc -O0 -shared -o jitter2infinitylib.dll -fPIC ../timer.c ../operations.c
