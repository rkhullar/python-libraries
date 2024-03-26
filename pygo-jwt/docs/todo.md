## Future Work
- [ ] adopt `pyproject.toml`
- [ ] integrate `cibuildwheel` with github actions
  - [x] build for linux and macos
  - [ ] automatic push to pypi
    - https://cibuildwheel.pypa.io/en/stable/deliver-to-pypi
- [ ] implement practical helpers:
    - [ ] encode tokens with claims `iss` `aud` `exp` `iat`, `nbf`
    - [ ] decode tokens with key server `PyJWKClient`
- [ ] improve error handling
    - [ ] remove `panic` in core logic
    - [ ] explore `panic` and `recover`
- [ ] research source distribution build
- [ ] test for windows?

### Blocked
- [ ] support alpine linux; remove skip
  - https://github.com/golang/go/issues/54805

### For PYGO Tools
- [ ] decouple patch logic to allow caller to define wheel path location?
- [ ] update `build-ffi` to include custom header files, like `wrapper_util.h`
