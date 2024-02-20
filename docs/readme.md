### TBD
- jwt-util: example python go library

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

## Useful Links
- [non-ai-licenses]

[non-ai-licenses]: https://github.com/non-ai-licenses/non-ai-licenses
