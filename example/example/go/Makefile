all: clean build

build:
	go build -buildmode=c-shared -o local/libhello.so main.go

clean:
	@rm -rf local
