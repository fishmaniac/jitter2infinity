from cffi import FFI as CFFI
from os import path


def get_lib(lib_name: str):
    import platform
    current_platform = platform.system()
    if current_platform == 'Windows':
        lib_name = path.abspath(path.join(
            './noise-sources/build/',
            lib_name + '.dll'
        ))
    elif current_platform == 'Linux' or current_platform == 'Darwin':
        lib_name = path.abspath(path.join(
            './noise-sources/build/',
            lib_name + '.so'
        ))
    else:
        raise OSError(
            f'Unknown platform {current_platform}, unable to link ffi.'
        )

    if not path.isfile(lib_name):
        raise FileNotFoundError(f'Library not found at path: {lib_name}')

    return lib_name


class FFI:
    def __init__(self, cdef: str, lib_name: str):
        lib_path = get_lib(lib_name=lib_name)

        self.ffi = CFFI()
        self.lib = self.ffi.dlopen(lib_path)
        self.ffi.cdef(cdef)
