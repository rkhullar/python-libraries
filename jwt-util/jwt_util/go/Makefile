all: clean build

build:
	go build -buildmode=c-shared -o local/libjwtutil.so wrapper.go core.go util.go main.go

clean:
	@rm -rf local

run:
	@go run main.go core.go util.go
