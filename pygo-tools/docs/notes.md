## Notes

### Additional Links
- https://github.com/rkhullar/python-java-scratches/tree/main/src/main/python/example-lib
- https://www.ardanlabs.com/blog/2020/07/extending-python-with-go.html
- https://dev.to/astagi/extending-python-with-go-1deb
- https://github.com/go-python/gopy
- https://pkg.go.dev/cmd/cgo
- https://pypi.org/project/cffi
- https://blog.kchung.co/faster-python-with-go-shared-objects
- https://cffi.readthedocs.io/en/latest/cdef.html
- https://last9.io/blog/using-golang-package-in-python-using-gopy
- https://www.nestorsag.com/blog/writing-c-extensions-for-python-with-cffi
- https://itwenty.me/posts/01-understanding-rpath

### Testing Wheel Validity
```shell
wheel unpack library.whl -d tmp
```

### Generating Project Structure
```shell
tree --charset ascii -I 'local|venv'
```

### Attempt to Embed Extension
```python
# attempt to build extension within package
module_name=f'{pkg_name}.lib.extension'
```

### Attempt to Ensure Non-Pure Build without Monkey Patching
```python
config_settings = config_settings or dict()
from wheel.bdist_wheel import get_platform
config_settings['--build-option'] = f'--plat-name {get_platform(None)} --py-limited-api cp312'
```

### File Extensions
#### Compiled Go
From the cffi [docs](https://cffi.readthedocs.io/en/latest/embedding.html) for embedding, the shared library should use
the following platform conventions:

|         |                     |
|---------|---------------------|
| linux   | `lib{plugin}.so`    |
| macos   | `lib{plugin}.dylib` |
| windows | `{plugin}.dll`      |

#### Python Extension
When the `build-ffi` script is used to create the python extension for the shared library, setuptools and cffi include it
in the wheel file with the following name for macos and linux: `{extension}.abi3.so`. On windows it looks like the name
would be `{extension.abi3.pyd`, but testing is required to confirm.
- [cffi.verifier._get_so_suffixes](https://github.com/python-cffi/cffi/blob/e59ec8f8b319874f6d063bee10ae87ae43016224/src/cffi/verifier.py#L292-L301)
