all: clean build

build:
	go build -buildmode=c-shared -o local/librsautil.so wrapper.go
	@# go tool cgo wrapper.go

clean:
	@rm -rf local

test:
	@go test

reset:
	@rm -f go.sum
	@go clean -modcache # remove download modules
	@go mod tidy # reinstall dependencies
