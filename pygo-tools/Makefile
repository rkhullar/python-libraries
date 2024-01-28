all: clean build post_build

build:
	python setup.py sdist bdist_wheel
	unzip -l dist/*.whl

clean:
	@rm -rf build dist *.egg-info

post_build:
	@rm -rf build *.egg-info
