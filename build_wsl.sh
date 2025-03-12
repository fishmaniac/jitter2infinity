#!/bin/bash

mkdir -p noise-sources/build && cd $_

x86_64-w64-mingw32-gcc -O0 -shared -o jitter2infinitylib.dll -fPIC ../timer.c ../operations.c
