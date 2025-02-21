#!/bin/bash
mkdir -p noise-sources/build && cd $_
gcc -O0 -shared -o jitter2infinitylib.so -fPIC ../main.c
x86_64-w64-mingw32-gcc -O0 -shared -o jitter2infinitylib.dll -fPIC ../main.c
