from setuptools.build_meta import build_wheel as _build_wheel
from .setup import precompile, patch_wheel_darwin, find_wheel


def build_wheel(*args, **kwargs):
    print('custom build_wheel')
    print(args)
    print(kwargs)
    return _build_wheel(*args, **kwargs)
