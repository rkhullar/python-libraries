build: clean build_sdist build_wheel post_build

build_sdist:
	python -m build -n --sdist
	tar -tvf dist/*.tar.gz

build_wheel:
	python -m build -n --wheel
	unzip -l dist/*.whl

clean:
	@rm -rf build dist *.egg-info

post_build:
	@rm -rf build *.egg-info
