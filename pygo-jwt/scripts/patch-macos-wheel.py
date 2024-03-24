from pygo_tools.setup import patch_wheel_darwin
from pygo_tools.util import monkey_patched
from pathlib import Path
from argparse import ArgumentParser, Namespace


def build_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('--wheel', required=True, type=Path)
    parser.add_argument('--dest-dir', required=True, type=Path)
    return parser


def copy_into_dir(source_file: Path, target_dir: Path) -> None:
    target_file = target_dir / source_file.name
    with source_file.open('rb') as s, target_file.open('wb') as t:
        t.write(s.read())


if __name__ == '__main__':
    parser: ArgumentParser = build_parser()
    args: Namespace = parser.parse_args()
    print(args)
