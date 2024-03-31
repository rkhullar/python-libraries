build: clean build_sdist build_wheel post_build


build_sdist:
	python -m build -n --sdist
	tar -tvf dist/*.tar.gz

build_wheel:
	python -m build -n --wheel
	unzip -l dist/*.whl

clean:
	@rm -rf build dist *.egg-info
	@rm -rf */go/local
	@rm -rf out

post_build:
	@rm -rf build *.egg-info

build_linux: clean
	cibuildwheel --config-file wheel.toml --platform linux --archs x86_64,aarch64

build_linux_amd64: clean
	cibuildwheel --config-file wheel.toml --platform linux --arch x86_64

build_linux_arm64: clean
	cibuildwheel --config-file wheel.toml --platform linux --arch aarch64

build_macos_amd64: clean
	cibuildwheel --config-file wheel.toml --platform macos --arch x86_64
	@make post_build

build_macos_arm64: clean
	cibuildwheel --config-file wheel.toml --platform macos --arch arm64
	@make post_build
