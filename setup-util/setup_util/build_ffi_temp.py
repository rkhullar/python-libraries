import sys
from pathlib import Path

from cffi import FFI

pkg_name, lib_name = 'jwt_util', 'jwtutil'
full_lib_name = f'lib{lib_name}'

path = Path(__file__).parent.absolute() / pkg_name / 'lib'
header_path, shared_object_path = path / f'{full_lib_name}.h', path / f'{full_lib_name}.so'


def build_extra_set_source_args() -> dict[str, list[str]]:
    match sys.platform:
        case 'linux':
            set_rpath = [f'-Wl,-rpath=$ORIGIN/{pkg_name}/lib']
            return dict(extra_link_args=set_rpath)
        case 'darwin':
            return dict()
        case _:
            return dict()


builder = FFI()

builder.set_source(
    module_name=f'{pkg_name}.lib.extension',
    source=f'#include "{header_path}"',
    libraries=[lib_name],
    library_dirs=[str(shared_object_path.parent)],
    **build_extra_set_source_args()
)

builder.cdef('''
    char* BuildSignature();
''')


if __name__ == '__main__':
    builder.compile(verbose=True, tmpdir='out')
