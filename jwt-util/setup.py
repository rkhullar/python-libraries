import subprocess
import sys
from pathlib import Path

from setuptools import find_packages, setup
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

pkg_name, lib_name = 'jwt_util', 'jwtutil'


def precompile():
    path = Path(__file__).parent.absolute() / pkg_name / 'go'
    subprocess.run('make', cwd=path)


def find_wheel() -> Path | None:
    dist_path = Path(__file__).parent.absolute() / 'dist'
    for path in dist_path.glob('*.whl'):
        return path


def patch_wheel_darwin():
    if wheel_path := find_wheel():
        dist_path = wheel_path.parent
        lib_file, ext_file = f'lib{lib_name}.so', 'extension.abi3.so'
        ext_path = Path(pkg_name) / 'lib' / ext_file
        commands = [
            ['unzip', str(wheel_path), ext_file],
            ['install_name_tool', '-change', lib_file, f'@loader_path/{pkg_name}/lib/{lib_file}', str(ext_path)],
            ['otool', '-L', str(ext_path)],
            ['zip', '-d', str(wheel_path), str(ext_path)],
            ['zip', '-u', str(wheel_path), str(ext_path)],
            ['rm', '-rf', pkg_name]
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
    cffi_modules=['build_ffi.py:builder'],
    install_requires=['cffi'],
    cmdclass={'bdist_wheel': BuildGoWheel}
)
