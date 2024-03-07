package core

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
