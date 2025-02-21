from cffi import FFI as CFFI
from os import path


def abspath(rel_path: str):
    return path.abspath(rel_path)


def get_lib():
    import platform
    current_platform = platform.system()
    if current_platform == 'Windows':
        lib_path = abspath('./noise-sources/build/jitter2infinitylib.dll')
    elif current_platform == 'Linux' or current_platform == 'Darwin':
        lib_path = abspath('./noise-sources/build/jitter2infinitylib.so')
    else:
        raise OSError(
            f"Unknown platform {current_platform}, unable to link ffi."
        )

    if not path.isfile(lib_path):
        raise FileNotFoundError(f"Library not found at path: {lib_path}")

    return lib_path


class FFI:
    def __init__(self, cdef: str):
        lib_path = get_lib()

        self.ffi = CFFI()
        self.lib = self.ffi.dlopen(lib_path)
        self.ffi.cdef(cdef)
