package main

import (
	"crypto/sha256"
	"encoding/hex"
	"log"
	"time"

	uuid "github.com/satori/go.uuid"
)

var (
	secureURL  = "/D2170E42-63B0-40ED-B0AE-9AF6CA3AC32E"
	secretText = ""
	salt       = "smart-or-strange"
)

func genUUID() {
	uuidRaw := uuid.NewV4().String()
	secureURL = "/" + uuidRaw

	secretRaw := sha256.Sum256([]byte(uuidRaw + salt))

	dst := make([]byte, hex.EncodedLen(len(secretRaw)))
	hex.Encode(dst, secretRaw[:])

	secretText = string(dst[:10])

	if *debugFlag {
		log.Printf("[secret] URL:%v Secret: %v \n", secureURL, secretText)
	}
}

func flashUUID() {
	d := time.Duration(time.Second * 60)
	t := time.NewTicker(d)
	defer t.Stop()
	genUUID()

	defer t.Stop()
	for {
		<-t.C
		genUUID()
	}
}
