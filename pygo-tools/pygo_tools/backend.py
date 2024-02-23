from setuptools import build_meta as _build_meta
from .config import Config
from .setup import patch_wheel_darwin, precompile, build_ffi, inject_file
import tempfile


def get_requires_for_build_wheel(config_settings=None):
    result = _build_meta.get_requires_for_build_wheel(config_settings)
    if 'cffi' not in result:
        result.append('cffi')
    return result


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    with tempfile.TemporaryDirectory() as temp_dir:
        config = Config.from_toml()
        precompile(config)
        source_ffi_path = build_ffi(config, target=temp_dir)
        print(source_ffi_path)
        result = _build_meta.build_wheel(wheel_directory, config_settings, metadata_directory)
        inject_file(config, path=source_ffi_path)
        # if config.platform == 'darwin':
        #     patch_wheel_darwin(config)
    return result
