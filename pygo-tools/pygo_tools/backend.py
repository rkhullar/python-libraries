from setuptools.build_meta import *
from setuptools import build_meta as _build_meta
from .config import Config
from .setup import patch_wheel_darwin, precompile, build_ffi, inject_file
import tempfile
from wheel.bdist_wheel import get_platform


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    config_settings = config_settings or dict()
    config_settings['--build-option'] = f'--plat-name {get_platform(None)} --py-limited-api cp312'
    with tempfile.TemporaryDirectory() as temp_dir:
        config = Config.from_toml()
        precompile(config)
        source_ffi_path = build_ffi(config, target=temp_dir)
        result = _build_meta.build_wheel(wheel_directory, config_settings, metadata_directory)
        inject_file(config, path=source_ffi_path)
        if config.platform == 'darwin':
            patch_wheel_darwin(config)
    return result
