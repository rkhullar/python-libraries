from cffi import FFI

from pygo_tools.config import Config

config = Config.load()
header_path, shared_object_path = config.header_path, config.shared_object_path


def build_extra_set_source_args() -> dict[str, list[str]]:
    match config.platform:
        case 'linux':
            set_rpath = [f'-Wl,-rpath=$ORIGIN/{config.package}/lib']
            return dict(extra_link_args=set_rpath)
        case 'darwin':
            return dict()
        case _:
            return dict()


builder = FFI()

'''
# attempt to build extension within package
module_name=f'{pkg_name}.lib.extension'
'''

builder.set_source(
    module_name=config.extension,
    source=f'#include "{header_path}"',
    libraries=[config.library],
    library_dirs=[str(config.library_path)],
    **build_extra_set_source_args()
)

builder.cdef('\n'.join(config.signatures))


def main():
    builder.compile(verbose=True, tmpdir='out')
