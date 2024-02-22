from setuptools import build_meta as _build_meta

from .setup import precompile, patch_wheel_darwin, find_wheel


def get_requires_for_build_wheel(config_settings=None):
    result = _build_meta.get_requires_for_build_wheel(config_settings)
    if 'cffi' not in result:
        result.append('cffi')
    return result


def build_wheel(*args, config_settings=None, **kwargs):
    print('custom build_wheel')
    print(args)
    print(kwargs)
    print("*"*100)
    print(config_settings)
    print("*"*100)
    return _build_meta.build_wheel(*args, **kwargs)
