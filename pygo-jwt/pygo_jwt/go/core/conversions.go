package core

import (
	"crypto/rsa"
	"github.com/rkhullar/python-libraries/pygo-jwt/pygo_jwt/go/util"
)

func NewJWK(size int, id *string) string {
	key := NewKey(size)
	return KeyToJSON(key, id)
}

func KeyToJSON(key *rsa.PrivateKey, id *string) string {
	data := KeyToMap(key, id)
	return util.MapToJSON(data)
}

func JWKToPEM(jwk string) string {
	key := ParseJWK(jwk)
	return KeyToPEM(key)
}

func PEMToJWK(data string, id *string) string {
	key := ParsePEM(data)
	return KeyToJSON(key, id)
}
