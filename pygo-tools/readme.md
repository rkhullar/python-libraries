## Python Golang Tools

This project aims to bridge the gap between Python and Golang, enabling developers to easily create high performance Python
libraries with precompiled Go extensions. `pygo-tools` wraps the `setup` function from `setuptools` and handles the process
of compiling your library's golang source before building the wheel file. `pygo-tools` also patches the resulting wheel file,
removing the need to manually configure `LD_LIBRARY_PATH` or `DYLD_LIBRARY_PATH`.

### Installation
```shell
pip install pygo-tools
```

### Example Usage
#### Project Structure
```text
|-- Makefile
|-- config.json
|-- example
|   |-- __init__.py
|   |-- go
|   |   |-- Makefile
|   |   `-- main.go
|   |-- lib -> go/local
|   `-- wrapper.py
|-- MANIFEST.in
|-- setup.py
`-- test.py
```

#### Project Config
`pygo-tools` looks for `config.json` at the root of your project. The config contains metadata like the python package name,
golang library, python extension, and `C` functon signatures for the underlying library.
```json
{
  "package": "example",
  "extension": "_example",
  "library": "hello",
  "signatures": [
    "char* Hello(char* name);"
  ]
}
```

#### Go
```go
// example/go/main.go

package main

import "C"
import "fmt"

func hello(message string, count int) string {
	return fmt.Sprintf("hello %s %d", message, count)
}

//export Hello
func Hello(message *C.char, count C.int) *C.char {
	result := hello(C.GoString(message), int(count))
	return C.CString(result)
}

func main() {}
```

```makefile
# example/go/Makefile

all: clean build

build:
	go build -buildmode=c-shared -o local/libhello.so main.go

clean:
	@rm -rf local
```

#### Python
```python
# example/wrapper.py

from _example import ffi, lib
from dataclasses import dataclass


@dataclass
class ExtensionAdapter:

    @staticmethod
    def hello(message: str, count: int = 1) -> str:
        params = ffi.new('char[]', message.encode()), ffi.cast('int', count)
        result = lib.Hello(*params)
        return ffi.string(result).decode()
```

```python
# example/__init__.py
from .wrapper import ExtensionAdapter
```

```python
# test.py

from example import ExtensionAdapter

adapter = ExtensionAdapter()
print(adapter.hello(message='world', count=4))
```

```python
# test.py

from pygo_tools import setup
from setuptools import find_packages

setup(
    name='example',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True
)
```

```text
# MANIFEST.in
include example/go/*.go
include example/lib/*.so
```

```makefile
all: clean build post_build

build:
	python setup.py bdist_wheel
	unzip -l dist/*.whl

clean:
	@rm -rf build dist *.egg-info
	@rm -rf */go/local

post_build:
	@rm -rf build *.egg-info
```

#### Build
The `Makefile` at the project level runs `setup.py bdist_wheel` in order to create the wheel file under the `dist` folder.
The binary distribution should include your python and golang source code, along with the compiled library and extension.
```text
- example/lib/libexample.so
- _example.abi3.so
```

#### Testing
Install the wheel file in your virtual environment and run `python test.py` to check that things are working end to end locally.
You can further test using with Docker or AWS Lambda. Note that the wheel file should be built for each platform (operating system
and architecture) that you want to support on runtime.

### Related Links
- https://cffi.readthedocs.io
