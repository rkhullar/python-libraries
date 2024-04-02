from argparse import ArgumentParser, Namespace
from pathlib import Path

from pygo_tools import Config, patch_wheel_darwin


def build_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('--wheel', required=True, type=Path)
    return parser


if __name__ == '__main__':
    parser: ArgumentParser = build_parser()
    args: Namespace = parser.parse_args()
    config = Config.load()
    patch_wheel_darwin(config=config, wheel_path=args.wheel)
