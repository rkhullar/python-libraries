import subprocess
from argparse import ArgumentParser, Namespace
from pathlib import Path

from pygo_tools import Config


def build_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('--wheel', required=True, type=Path)
    return parser


def patch_wheel_darwin(wheel_path: Path, config: Config):
    dist_path = wheel_path.parent
    lib_file, ext_file = f'lib{config.library}.so', f'{config.extension}.abi3.so'
    commands = [
            ['unzip', str(wheel_path), ext_file],
            ['install_name_tool', '-change', lib_file, f'@loader_path/{config.package}/lib/{lib_file}', ext_file],
            ['otool', '-L', ext_file],
            ['zip', '-d', str(wheel_path), ext_file],
            ['zip', '-u', str(wheel_path), ext_file],
            ['rm', '-rf', ext_file]
        ]
    for command in commands:
        subprocess.run(command, cwd=dist_path)


if __name__ == '__main__':
    parser: ArgumentParser = build_parser()
    args: Namespace = parser.parse_args()
    config = Config.load()
    patch_wheel_darwin(wheel_path=args.wheel, config=config)
