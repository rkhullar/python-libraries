## TODO

### Revisit Auth Helpers
- [x] test auth0 flow
- [ ] test okta flow
- [ ] test cognito flow
- [ ] improve abstract bearer
  - [ ] decouple params from parent `OAuth2AuthorizationCodeBearer`
  - [ ] allow kwargs in constructor?
  - [ ] move call to `super().__init__` from child to abstract class?
  - [ ] add abstract method for setup before constructor?
- check common params
  - [ ] scopes
  - [ ] auto_error
- decide if scopes should be excluded setup if undefined, or defaulted
- move logic for building `require_scopes`, `allowed_scopes` outside of `build_auth_depends`?
- use case for different auth types?
  - more than one type of JWT access token
  - api key auth type

### Revisit MongoDB Helper
- [ ] rename package from `mongo` to `mongodb`?
- [ ] rename `build_atlas_client` to specify aws integration
- [ ] create other helpers for gcp and azure?
- [ ] reorganize utils?
- [ ] move package under parent `db` or `database`?
- [ ] support integration with `pymongo` or `motor`?

### Revisit Middleware
- [ ] improve process time header flow:
  - `# app.add_middleware(add_process_time_header)`
  - `app.middleware('http')(add_process_time_header)`
