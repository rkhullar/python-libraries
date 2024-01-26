all: clean build

build:
	go build -buildmode=c-shared -o local/libjwtutil.so main.go wrapper.go

clean:
	@rm -rf local
