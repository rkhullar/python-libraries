import os
from argparse import ArgumentParser, Namespace

from cffi import FFI

from pygo_tools.config import Config


def build_extra_set_source_args(config: Config) -> dict[str, list[str]]:
    match config.platform:
        case 'linux':
            set_rpath = [f'-Wl,-rpath=$ORIGIN/{config.package}/lib']
            return dict(extra_link_args=set_rpath)
        case 'darwin':
            return dict()
        case _:
            return dict()


def dynamic_builder(config: Config):
    builder = FFI()
    builder.set_source(
        module_name=config.extension,
        source=f'#include "{config.header_path}"',
        libraries=[config.library],
        library_dirs=[str(config.library_path)],
        include_dirs=[str(config.library_source_path)],  # used to find header paths
        **build_extra_set_source_args(config)
    )
    builder.cdef('\n'.join(config.signatures))
    return builder


def build_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('--mode', choices=['json', 'toml'], required=False)
    parser.add_argument('--target', default='out')
    return parser


def main():
    parser: ArgumentParser = build_parser()
    args: Namespace = parser.parse_args()
    config = Config.load(mode=args.mode)
    builder = dynamic_builder(config)
    builder.compile(verbose=True, tmpdir=args.target)


if __name__ == '__cffi__':
    if config_path := os.environ.get('PYGO_CONFIG_PATH'):
        print("*"*100)
        print(f'detected {config_path=}; might support in future release')
        print("*"*100)
    default_config = Config.load()
    default_builder = dynamic_builder(default_config)
