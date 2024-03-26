build: clean
	go build -buildmode=c-shared -o local/librsautil.so wrapper.go wrapper_util.go
	@# go tool cgo wrapper.go wrapper_util.go

clean:
	@rm -rf local _obj

test: clean
	@go test

reset: clean
	@rm -f go.sum
	@go clean -modcache # remove download modules
	@go mod tidy # reinstall dependencies
