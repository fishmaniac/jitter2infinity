#!/bin/bash

mkdir -p noise-sources/build && cd $_

gcc -O0 -shared -o jitter2infinitylib.so -fPIC ../timer.c ../operations.c
