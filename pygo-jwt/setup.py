from pathlib import Path

from pygo_tools import setup
from setuptools import find_packages


def read_file(path: Path | str) -> str:
    with Path(path).open('r') as f:
        return f.read().strip()


setup(
    name='pygo-jwt',
    version='0.0.8',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.10, <4.0',
    author='Rajan Khullar',
    author_email='rkhullar03@gmail.com',
    license='MIT NON-AI',
    description="Encode and Decode RS256 JSON Web Tokens with Python and Go",
    long_description=read_file('readme.md'),
    long_description_content_type='text/markdown',
    project_urls={
        'Source': 'https://github.com/rkhullar/python-libraries/tree/main/pygo-jwt'
    }
)

# TODO: define config_path?
