package main

import (
	"crypto/rand"
	"crypto/rsa"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"math/big"
)

func b64enc(data []byte) string {
	return base64.RawURLEncoding.EncodeToString(data)
}

func build_key(size int) string {
	private_key, err := rsa.GenerateKey(rand.Reader, size)
	if err != nil {
		panic(err)
	}
	E := big.NewInt(int64(private_key.E))
	private_jwk := map[string]interface{}{
		"kty": "RSA",
		"n":   b64enc(private_key.N.Bytes()),
		"e":   b64enc(E.Bytes()),
		"d":   b64enc(private_key.D.Bytes()),
		"p":   b64enc(private_key.Primes[0].Bytes()),
		"q":   b64enc(private_key.Primes[1].Bytes()),
		"dp":  b64enc(private_key.Precomputed.Dp.Bytes()),
		"dq":  b64enc(private_key.Precomputed.Dq.Bytes()),
		"qi":  b64enc(private_key.Precomputed.Qinv.Bytes()),
	}
	private_jwk_json, err := json.Marshal(private_jwk)
	if err != nil {
		panic(err)
	}
	return string(private_jwk_json)
}

func build_signature() string {
	return "hello world"
}

func main() {
	jwk := build_key(2048)
	fmt.Println(jwk)
}

/*
	privateKey, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		fmt.Println("Error generating RSA key pair:", err)
		return
	}

	publicKey := &privateKey.PublicKey

	// Message to be signed
	message := []byte("message")

	// Sign the message using the private key
	signature, err := rsa.SignPKCS1v15(rand.Reader, privateKey, crypto.SHA256, sha256.Sum256(message))
	if err != nil {
		fmt.Println("Error signing message:", err)
		return
	}

	// Verify the signature using the public key
	err = rsa.VerifyPKCS1v15(publicKey, crypto.SHA256, sha256.Sum256(message), signature)
	if err != nil {
		fmt.Println("Signature verification failed:", err)
		return
	}

	fmt.Println("Signature verification successful!")
*/
