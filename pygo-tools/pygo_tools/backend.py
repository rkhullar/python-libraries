import tempfile

from setuptools import build_meta as _build_meta
from setuptools.build_meta import *
from wheel.bdist_wheel import bdist_wheel
from pathlib import Path

from .config import Config
from .setup import build_ffi, inject_file, patch_wheel_darwin, precompile,find_wheel
from .util import monkey_patched


class custom_bdist_wheel(bdist_wheel):
    def finalize_options(self):
        # NOTE: self.distribution -> setuptools.dist.Distribution
        self.root_is_pure = False
        install_requires: list[str] = self.distribution.install_requires
        for dep in ['cffi']:
            if dep not in install_requires:
                install_requires.append(dep)

    def run(self):
        print('hook before base run')
        result = super(self).run()
        print('hook after base run')
        return result


@monkey_patched(original=bdist_wheel, extended=custom_bdist_wheel, to_patch=['finalize_options'])
def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    with tempfile.TemporaryDirectory() as temp_dir:
        config = Config.from_toml()
        precompile(config)
        source_ffi_path = build_ffi(config, target=temp_dir)
        result = _build_meta.build_wheel(wheel_directory, config_settings, metadata_directory)
        inject_file(config, path=source_ffi_path)
        if config.platform == 'darwin':
            print('='*100)
            print(wheel_directory)
            print(type(wheel_directory))
            print()
            print('='*100)
            wheel_path = find_wheel(config, dist_path=Path(wheel_directory))
            if not wheel_path:
                raise FileNotFoundError(f'could not find wheel to patch')
            patch_wheel_darwin(config, wheel_path=wheel_path)
    return result
