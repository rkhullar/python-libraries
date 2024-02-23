from setuptools.build_meta import *
from setuptools import build_meta as _build_meta
from .config import Config
from .setup import patch_wheel_darwin, precompile, build_ffi, inject_file
import tempfile


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    with tempfile.TemporaryDirectory() as temp_dir:
        config = Config.from_toml()
        precompile(config)
        source_ffi_path = build_ffi(config, target=temp_dir)
        result = _build_meta.build_wheel(wheel_directory, config_settings, metadata_directory)
        inject_file(config, path=source_ffi_path)
        if config.platform == 'darwin':
            patch_wheel_darwin(config)
    return result


''' TODO
- [ ] add cffi to install_requires
- [ ] mark wheel file as non-pure python
- [ ] fix sha256sum hashes for so files?
- [ ] add extension to top level record?
'''
