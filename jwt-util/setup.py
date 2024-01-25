import subprocess
import sys
from pathlib import Path

from setuptools import find_packages, setup
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


def precompile():
    path = Path(__file__).parent.absolute() / 'example'
    subprocess.run('make', cwd=path)


def find_wheel() -> Path | None:
    dist_path = Path(__file__).parent.absolute() / 'dist'
    for path in dist_path.glob('*.whl'):
        return path


def patch_wheel_darwin():
    if wheel_path := find_wheel():
        dist_path = wheel_path.parent
        to_patch = '_example.abi3.so'
        commands = [
            ['unzip', str(wheel_path), to_patch],
            ['install_name_tool', '-change', 'libexample.so', '@loader_path/example/lib/libexample.so', to_patch],
            ['otool', '-L', to_patch],
            ['zip', '-d', str(wheel_path), to_patch],
            ['zip', '-u', str(wheel_path), to_patch],
            ['rm', to_patch]
        ]
        for command in commands:
            subprocess.run(command, cwd=dist_path)


class BuildGoWheel(_bdist_wheel):
    def run(self):
        precompile()
        _bdist_wheel.run(self)
        if sys.platform == 'darwin':
            patch_wheel_darwin()


setup(
    name='jwt-util',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    cffi_modules=['example/build_ffi.py:builder'],
    install_requires=['cffi'],
    cmdclass={'bdist_wheel': BuildGoWheel}
)
