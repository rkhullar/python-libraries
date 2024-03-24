## Building
```shell
cd pydantic-mql
python setup.py sdist bdist_wheel
rm -rf build pydantic_mql.egg-info
```

## Publishing
```shell
cd pydantic-mql
twine upload -r testpypi dist/*
twine upload dist/*
```

## Install from GitHub
```shell
# https://pip.pypa.io/en/stable/cli/pip_install/#pip-install-examples
# example: install pygo-tools from branch feature/toml
pip install 'pygo-tools @ git+https://github.com/rkhullar/python-libraries.git@feature/toml#subdirectory=pygo-tools'
```

## Install from Source Distribution (wip)
```shell
pip install cython
pip install meson-python
pip install numpy --no-binary ':all:'
# did not wok
```

## Useful Links
- [non-ai-licenses]

[non-ai-licenses]: https://github.com/non-ai-licenses/non-ai-licenses
