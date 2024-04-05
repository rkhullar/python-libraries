build: clean
	go build -buildmode=c-shared -o local/libhello.so core.go wrapper.go

clean:
	@rm -rf local

test: clean
	@go test

reset: clean
	@rm -f go.sum
	@go clean -modcache # remove download modules
	@go mod tidy # reinstall dependencies
