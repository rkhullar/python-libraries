## Python Golang Tools

This project aims to bridge the gap between Python and Golang, enabling developers to easily create high performance Python
libraries with precompiled Go extensions. `pygo-tools` wraps the `setup` function from `setuptools` and handles the process
of compiling your library's golang source before building the wheel file. `pygo-tools` also patches the resulting extension,
removing the need to manually configure `LD_LIBRARY_PATH` or `DYLD_LIBRARY_PATH` before runtime.

### Installation
```shell
pip install pygo-tools
```

### Example Projects
- [hello world with `setup.py` and `config.json`][hello-v1]
- [hello world with `pyproject.toml`][hello-v2]

### Walkthrough for Hello World with `setup.py` and `config.json`
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
    "char* Hello(char* message, int count);"
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
# setup.py

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
	python -m build -n --wheel
	unzip -l dist/*.whl

clean:
	@rm -rf build dist *.egg-info
	@rm -rf */go/local

post_build:
	@rm -rf build *.egg-info
```

#### Build
The `Makefile` at the project level runs `python -m build -n --wheel` in order to create the wheel file under the `dist` folder.
The binary distribution should include your python and golang source code, along with the compiled library and extension.
```text
- example/lib/libhello.so
- _example.abi3.so
```

#### Testing
Install the wheel file in your virtual environment and run `python test.py` to check that things are working end to end locally.

#### Distributing
Binary distributions with compiled code should be built for each platform that you want to support during runtime. [`cibuildwheel`]
can be used for this. However, you can also create a `Dockerfile` and `docker-compose.yaml` to build wheels for `linux/arm64`
and `linux/amd64`:

```dockerfile
# Dockerfile
ARG PYTHON_VERSION=3.12
FROM public.ecr.aws/sam/build-python${PYTHON_VERSION}
RUN dnf install -y golang make
RUN pip install -U pip setuptools
RUN pip install pygo-tools
COPY example example/
COPY setup.py config.json MANIFEST.in ./
RUN python -m build -n --wheel
ENTRYPOINT ["/bin/sh"]
```

```yaml
# docker-compose.yaml
version: '3'
services:
  builder:
    build: .
    platform: linux/arm64
    volumes:
      - ./out:/var/task/out:rw
    entrypoint: ["/bin/sh", "-c"]
    command: ["cp dist/* out/"]
```

### Related Links
- [cffi]
- [cibuildwheel]

[cffi]: https://cffi.readthedocs.io
[cibuildwheel]: https://cibuildwheel.readthedocs.io
[hello-v1]: https://github.com/rkhullar/python-libraries/tree/main/examples/pygo-tools/hello-v1
[hello-v2]: https://github.com/rkhullar/python-libraries/tree/main/examples/pygo-tools/hello-v2
