import os
import subprocess
from pathlib import Path

from setuptools import setup as _setup
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

from .config import Config


def precompile(config: Config):
    subprocess.run('make', cwd=config.library_source_path)


def find_wheel(config: Config) -> Path | None:
    dist_path = config.project_path / 'dist'
    for path in dist_path.rglob('*.whl'):
        return path


def build_ffi(config: Config, target: str = None, rename: bool = True) -> Path | None:
    command = ['build-ffi']
    if target:
        command.extend(['--target', target])
    subprocess.run(command, cwd=config.project_path)
    search_path = Path(target) if target else Path()
    for path in search_path.rglob('*.so'):
        if rename:
            path = path.rename(search_path / config.extension_path.name)
        return path


def inject_file(config: Config, path: Path):
    """helper needed for newer build format with toml"""
    if wheel_path := find_wheel(config):
        dist_path = wheel_path.parent
        commands = [
            ['zip', '-j', str(wheel_path), str(path)],
        ]
        for command in commands:
            subprocess.run(command, cwd=dist_path)


def patch_wheel_darwin(config: Config):
    if wheel_path := find_wheel(config):
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
        config = Config.from_json()
        precompile(config)
        _bdist_wheel.run(self)
        if config.platform == 'darwin':
            patch_wheel_darwin(config)


def setup(cffi: str = 'cffi', config_path: str = None, **kwargs):
    if config_path:
        os.environ['PYGO_CONFIG_PATH'] = config_path
    cmdclass = kwargs.pop('cmdclass', dict())
    install_requires = kwargs.get('install_requires', list())
    cmdclass['bdist_wheel'] = BuildGoWheel
    if cffi not in install_requires:
        install_requires.append(cffi)
    build_ffi_path = Path(__file__).parent / 'build_ffi.py'
    cffi_module = f'{build_ffi_path}:default_builder'
    _setup(**kwargs, cmdclass=cmdclass, install_requires=install_requires, cffi_modules=[cffi_module])
