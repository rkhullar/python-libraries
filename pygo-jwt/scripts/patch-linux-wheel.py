from argparse import ArgumentParser, Namespace
from pathlib import Path
import subprocess
from pygo_tools import Config


def build_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('--wheel', required=True, type=Path)
    return parser


def patch_wheel_linux(config: Config, wheel_path: Path):
    dist_path = wheel_path.parent
    lib_file = f'lib{config.library}.so'
    commands = [
        ['unzip', '-l', str(wheel_path)]
        # ['zip', '-d', str(wheel_path), lib_file],
    ]
    for command in commands:
        subprocess.run(command, cwd=dist_path)


if __name__ == '__main__':
    parser: ArgumentParser = build_parser()
    args: Namespace = parser.parse_args()
    config = Config.load()
    patch_wheel_linux(config, wheel_path=args.wheel)
