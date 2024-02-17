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
