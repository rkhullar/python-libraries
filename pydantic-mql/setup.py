from pathlib import Path

import pipfile
from setuptools import find_packages, setup


def read_file(path: Path | str) -> str:
    with Path(path).open('r') as f:
        return f.read().strip()


def load_requirements() -> list[str]:
    return [f'{package}{version}' for package, version in pipfile.load().data['default'].items()]


def read_python_version() -> str:
    return pipfile.load().data['_meta']['requires']['python_version']


setup(
    name='pydantic-mql',
    version=read_file('version.txt'),
    url='https://github.com/rkhullar/python-libraries/tree/main/pydantic-mql',
    author='Rajan Khullar',
    author_email='rkhullar03@gmail.com',
    long_description=read_file('readme.md'),
    long_description_content_type='text/markdown',
    # keywords='',
    license='MIT NON-AI',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    python_requires='~='+read_python_version(),
    install_requires=load_requirements(),
    include_package_data=True,
    zip_safe=False,
    # test_suite='nose.collector',
    # tests_require=['nose', 'parameterized'],
    entry_points={}
)
