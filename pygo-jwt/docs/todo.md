## Future Work
- [ ] adopt `pyproject.toml`
- [ ] integrate `cibuildwheel` with github actions
- [ ] implement practical helpers:
    - [ ] encode tokens with claims `iss` `aud` `exp` `iat`, `nbf`
    - [ ] decode tokens with key server `PyJWKClient`
- [ ] research source distribution build

### Blocked
- [ ] support alpine linux; remove skip
  - https://github.com/golang/go/issues/54805
