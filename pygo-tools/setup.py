from pathlib import Path

from setuptools import find_packages, setup


def read_file(path: Path | str) -> str:
    with Path(path).open('r') as f:
        return f.read().strip()


setup(
    name='pygo-tools',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['build-ffi=pygo_tools.build_ffi:main']},
    python_requires='~=3.12',
    install_requires=['build', 'setuptools', 'wheel', 'toml', 'cffi'],
    author='Rajan Khullar',
    author_email='rkhullar03@gmail.com',
    license='MIT NON-AI',
    description='Simplify Python-Go integration for Libraries with Precompiled Extensions',
    long_description=read_file('readme.md'),
    long_description_content_type='text/markdown',
    project_urls={
        'Source': 'https://github.com/rkhullar/python-libraries/tree/main/pygo-tools'
    }
)
