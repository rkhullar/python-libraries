import subprocess
import sys
from pathlib import Path

from setuptools import setup as _setup
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

from .config import Config

config = Config.load()


def precompile():
    path = config.project_path / config.package / 'go'
    subprocess.run('make', cwd=path)


def find_wheel() -> Path | None:
    dist_path = config.project_path / 'dist'
    for path in dist_path.glob('*.whl'):
        return path


def patch_wheel_darwin():
    if wheel_path := find_wheel():
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


class BuildGoWheel(_bdist_wheel):
    def run(self):
        precompile()
        _bdist_wheel.run(self)
        if sys.platform == 'darwin':
            patch_wheel_darwin()


def setup(cffi: str = 'cffi', **kwargs):
    cmdclass = kwargs.pop('cmdclass', dict())
    install_requires = kwargs.get('install_requires', list())
    cmdclass['bdist_wheel'] = BuildGoWheel
    if cffi not in install_requires:
        install_requires.append(cffi)
    build_ffi_path = Path(__file__).parent / 'build_ffi.py'
    cffi_module = f'{build_ffi_path}:builder'
    _setup(**kwargs, cmdclass=cmdclass, install_requires=install_requires, cffi_modules=[cffi_module])
