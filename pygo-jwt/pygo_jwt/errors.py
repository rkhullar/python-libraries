class TokenDecodeError(Exception):
    pass


class InvalidSignature(TokenDecodeError):
    pass
