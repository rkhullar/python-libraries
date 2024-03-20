package core

import (
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"github.com/rkhullar/python-libraries/jwt-util/jwt_util/go/util"
)

func Sign(key *rsa.PrivateKey, data string) string {
	result, err := rsa.SignPKCS1v15(rand.Reader, key, crypto.SHA256, util.SHA256Sum(data))
	if err != nil {
		panic(err)
	}
	return util.B64Enc(result)
}

func ParseJWKAndSign(jwk string, data string) string {
	key := ParseJWK(jwk)
	return Sign(key, data)
}

func ParsePEMAndSign(pem string, data string) string {
	key := ParsePEM(pem)
	return Sign(key, data)
}
