package core

import (
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"github.com/rkhullar/python-libraries/jwt-util/jwt_util/go/util"
	"math/big"
)

func PublicKeyToMap(key *rsa.PublicKey, id *string) util.StringMap {
	E := big.NewInt(int64(key.E))
	data := util.StringMap{
		"kty": "RSA",
		"e":   util.B64Enc(E.Bytes()),
		"n":   util.B64Enc(key.N.Bytes()),
		"alg": "RS256",
		"use": "sig",
	}
	if id != nil {
		data["kid"] = *id
	}
	return data
}

func PublicKeyToJSON(key *rsa.PublicKey, id *string) string {
	data := PublicKeyToMap(key, id)
	return util.MapToJSON(data)
}

func PublicKeyToPEM(key *rsa.PublicKey) string {
	// TODO: consider PKIX format?
	data := pem.EncodeToMemory(&pem.Block{
		Type:  "RSA PUBLIC KEY",
		Bytes: x509.MarshalPKCS1PublicKey(key),
	})
	return string(data)
}

func ExtractPublicJWK(jwk string) string {
	data := util.ParseJSON(jwk)
	key := ParseMap(data)
	kid := util.StringMap_GetStrPtr(data, "kid")
	return PublicKeyToJSON(&key.PublicKey, kid)
}

func ExtractPublicPEM(pem string) string {
	key := ParsePEM(pem)
	return PublicKeyToPEM(&key.PublicKey)
}
