package core

import (
	"crypto/rsa"
	"github.com/rkhullar/python-libraries/pygo-jwt/pygo_jwt/go/util"
)

func NewJWK(size int, id *string) (string, error) {
	key, err := NewKey(size)
	if err != nil {
		return "", err
	}
	return KeyToJSON(key, id)
}

func KeyToJSON(key *rsa.PrivateKey, id *string) (string, error) {
	data := KeyToMap(key, id)
	return util.MapToJSON(data)
}

func JWKToPEM(jwk string) (string, error) {
	key, err := ParseJWK(jwk)
	if err != nil {
		return "", err
	}
	return KeyToPEM(key)
}

func PEMToJWK(data string, id *string) (string, error) {
	key, err := ParsePEM(data)
	if err != nil {
		return "", err
	}
	return KeyToJSON(key, id)
}
