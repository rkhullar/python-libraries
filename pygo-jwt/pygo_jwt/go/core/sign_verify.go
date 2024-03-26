package core

import (
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"github.com/rkhullar/python-libraries/pygo-jwt/pygo_jwt/go/util"
)

func Sign(key *rsa.PrivateKey, data string) (string, error) {
	result, err := rsa.SignPKCS1v15(rand.Reader, key, crypto.SHA256, util.SHA256Sum(data))
	if err != nil {
		return "", err
	}
	return util.B64Enc(result), nil
}

func Verify(key *rsa.PublicKey, data string, signature string) (bool, error) {
	signature_data, err := util.B64Dec(signature)
	if err != nil {
		return false, err
	}
	err = rsa.VerifyPKCS1v15(key, crypto.SHA256, util.SHA256Sum(data), signature_data)
	return err == nil, nil
}

func ParseJWKAndSign(jwk string, data string) (string, error) {
	key, err := ParseJWK(jwk)
	if err != nil {
		return "", err
	}
	return Sign(key, data)
}

func ParsePEMAndSign(pem string, data string) (string, error) {
	key, err := ParsePEM(pem)
	if err != nil {
		return "", err
	}
	return Sign(key, data)
}

func ParsePublicJWKAndVerify(jwk string, data string, signature string) (bool, error) {
	key, err := ParsePublicJWK(jwk)
	if err != nil {
		return false, err
	}
	return Verify(key, data, signature)
}

func ParsePublicPEMAndVerify(pem string, data string, signature string) (bool, error) {
	key, err := ParsePublicPEM(pem)
	if err != nil {
		return false, err
	}
	return Verify(key, data, signature)
}
