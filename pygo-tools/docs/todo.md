## TODO
- [x] mark wheel file as non-pure python
  - done with monkey patch on `bdist_wheel` class
- [x] add `cffi` to `install_requires`
- [ ] fix `sha256sum` hashes for so files?
- [ ] add extension to top level record?
- [ ] include changelog in build?

## Ideas
- [ ] build context manager class for patching wheel files:
  - unzips to temporary directory during operations
  - rezip into original file after operations
  - insert / update file; ignore source path parents; allow optional target path
  - add requirement to `METADATA` `Requires-Dist`
  - add package / module to `top_level.txt`
  - generate `sha256sum` hash for file; upsert to `RECORD`

## Revisit Custom Backend
- [ ] try `finalize_distribution_options`
  - https://setuptools.pypa.io/en/latest/userguide/extension.html#customizing-distribution-options
