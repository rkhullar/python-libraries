```shell
pip install -U pip
pip install build
pip install setuptools
pip install wheel
pip install ../pygo-tools-v2
```

```shell
python -m build -n --sdist
python -m build -n --wheel
```