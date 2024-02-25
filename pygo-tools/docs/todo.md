## TODO
- [x] mark wheel file as non-pure python
  - done with monkey patch on `bdist_wheel` class
- [x] add `cffi` to `install_requires`
- [ ] fix `sha256sum` hashes for so files?
- [ ] add extension to top level record?
- [ ] include changelog in build?
- [ ] test examples against aws lambda
- [ ] transfer or include [`example-lib`](https://github.com/rkhullar/python-java-scratches/tree/main/src/main/python/example-lib)?

## Ideas
- [ ] build context manager class for patching wheel files:
  - unzips to temporary directory during operations
  - rezip into original file after operations
  - insert / update file; ignore source path parents; allow optional target path
  - add requirement to `METADATA` `Requires-Dist`
  - add package / module to `top_level.txt`
  - generate `sha256sum` hash for file; upsert to `RECORD`

- [ ] entrypoint for starting project? 
  - main entrypoint would be like `pygo-tool`
  - subparser command for `start-project`
  - reads config from params or from stdin?
  - another subparser for `build-ffi`
  - remove `build-ffi` entrypoint?


### Revisit Custom Backend
- [ ] try `finalize_distribution_options`
  - https://setuptools.pypa.io/en/latest/userguide/extension.html#customizing-distribution-options
