from setuptools import build_meta as _build_meta
from .setup import precompile, patch_wheel_darwin, find_wheel


def get_requires_for_build_wheel(config_settings=None):
    result = _build_meta.get_requires_for_build_wheel(config_settings)
    if 'cffi' not in result:
        result.append('cffi')
    return result


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    print('custom build_wheel')
    print("*"*100)
    print(wheel_directory)
    print(config_settings)
    print(metadata_directory)
    print("*"*100)
    return _build_meta.build_wheel(wheel_directory, config_settings, metadata_directory)
