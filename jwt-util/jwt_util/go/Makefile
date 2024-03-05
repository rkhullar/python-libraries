all: clean build

build:
	go build -buildmode=c-shared -o local/libjwtutil.so wrapper.go

clean:
	@rm -rf local

run:
	@go run main_example.go

test:
	@go run main_test.go
