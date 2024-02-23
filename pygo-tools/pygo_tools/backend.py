from setuptools import build_meta as _build_meta
from .setup import precompile, patch_wheel_darwin
from .config import Config


def get_requires_for_build_wheel(config_settings=None):
    result = _build_meta.get_requires_for_build_wheel(config_settings)
    if 'cffi' not in result:
        result.append('cffi')
    return result


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    config = Config.from_toml()
    precompile(config)
    result = _build_meta.build_wheel(wheel_directory, config_settings, metadata_directory)
    # if config.platform == 'darwin':
    #     patch_wheel_darwin(config)
    return result
