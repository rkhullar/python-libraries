from setuptools.build_meta import build_sdist as _build_sdist
from setuptools.build_meta import build_wheel as _build_wheel


def build_sdist(*args, **kwargs):
    print('custom build_sdist')
    print(args)
    print(kwargs)
    return _build_sdist(*args, **kwargs)


def build_wheel(*args, **kwargs):
    print('custom build_wheel')
    print(args)
    print(kwargs)
    return _build_wheel(*args, **kwargs)
