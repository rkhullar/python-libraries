all: clean build post_build

build:
	python -m build -n --wheel --config-setting x=1
	unzip -l dist/*.whl

clean:
	@rm -rf build dist *.egg-info
	@rm -rf */go/local

post_build:
	@rm -rf build *.egg-info
