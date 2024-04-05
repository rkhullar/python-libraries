from .config import Config
from .setup import build_ffi
from setuptools.command.build_ext import build_ext


class CustomBuildExtCommand(build_ext):
    def run(self):
        print('='*100)
        print('before build ext run')
        print('='*100)
        build_ext.run(self)
        print('='*100)
        print('after build ext run')
        print('='*100)
