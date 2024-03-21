package core

import (
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"github.com/rkhullar/python-libraries/pygo-jwt/pygo_jwt/go/util"
)

func Sign(key *rsa.PrivateKey, data string) string {
	result, err := rsa.SignPKCS1v15(rand.Reader, key, crypto.SHA256, util.SHA256Sum(data))
	if err != nil {
		panic(err)
	}
	return util.B64Enc(result)
}

func Verify(key *rsa.PublicKey, data string, signature string) bool {
	err := rsa.VerifyPKCS1v15(key, crypto.SHA256, util.SHA256Sum(data), util.B64Dec(signature))
	return err == nil
}

func ParseJWKAndSign(jwk string, data string) string {
	key := ParseJWK(jwk)
	return Sign(key, data)
}

func ParsePEMAndSign(pem string, data string) string {
	key := ParsePEM(pem)
	return Sign(key, data)
}

func ParsePublicJWKAndVerify(jwk string, data string, signature string) bool {
	key := ParsePublicJWK(jwk)
	return Verify(key, data, signature)
}

func ParsePublicPEMAndVerify(pem string, data string, signature string) bool {
	key := ParsePublicPEM(pem)
	return Verify(key, data, signature)
}
