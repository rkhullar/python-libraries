all: clean build

build:
	go build -buildmode=c-shared -o local/libjwtutil.so wrapper.go
	@# go tool cgo wrapper.go

clean:
	@rm -rf local

run:
	@go run main_example.go

test:
	@go test main_test.go

reset:
	@rm -f go.sum
	@go clean -modcache # remove download modules
	@go mod tidy # reinstall dependencies
