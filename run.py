import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test')
sys.path.append(test_dir)
from jitter import main


def compile(cmd: str):
    print('Running:', ' '.join(cmd))
    subprocess.run(cmd)


def build():
    build_dir = 'noise-sources/build'
    lib_name = 'jitter2infinitylib'
    so = '.so'
    dll = '.dll'

    gcc = 'gcc'
    mingw = 'x86_64-w64-mingw32-gcc'
    flags = ['-shared', '-fpic', '-fno-strict-aliasing', '-fno-inline']
    optimization_levels = ['-O0', '-O1', '-O2', '-O3', '-Ofast', '-Og', '-Os']
    source_files = ['noise-sources/timer.c', 'noise-sources/operations.c']

    try:
        os.mkdir(build_dir)
    except OSError as e:
        print('Mkdir: ', e)

    with ThreadPoolExecutor() as executor:
        futures = []
        for opt in optimization_levels:
            lib_name_opt = lib_name + opt
            gcc_cmd = [gcc] + flags + [
                opt,
                '-o',
                os.path.join(build_dir, lib_name_opt + so)
            ] + source_files

            if os.name == 'nt':
                gcc_cmd = ['wsl', '--'] + gcc_cmd

            mingw_cmd = [mingw] + flags + [
                opt,
                '-o',
                os.path.join(build_dir, lib_name_opt + dll)
            ] + source_files

            if os.name == 'nt':
                mingw_cmd = ['wsl', '--'] + mingw_cmd

            futures.append(executor.submit(compile, gcc_cmd))
            futures.append(executor.submit(compile, mingw_cmd))

        for future in futures:
            future.result()


if __name__ == '__main__':
    build()
    print("Starting...")
    main()
