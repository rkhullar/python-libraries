import tempfile

from setuptools import build_meta as _build_meta
from setuptools.build_meta import *
from wheel.bdist_wheel import bdist_wheel

from .config import Config
from .setup import build_ffi, inject_file, patch_wheel_darwin, precompile
from .util import monkey_patched


class custom_bdist_wheel(bdist_wheel):
    def finalize_options(self):
        # NOTE: self.distribution -> setuptools.dist.Distribution
        self.root_is_pure = False
        install_requires: list[str] = self.distribution.install_requires
        for dep in ['cffi']:
            if dep not in install_requires:
                install_requires.append(dep)


@monkey_patched(original=bdist_wheel, extended=custom_bdist_wheel, to_patch=['finalize_options'])
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
