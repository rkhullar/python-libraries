class PyGoJWTError(Exception):
    pass


class TokenDecodeError(PyGoJWTError):
    pass


class InvalidSignatureError(TokenDecodeError):
    pass
