package main

import (
	"flag"
	"log"
)

var (
	addrFlag  = flag.String("listen", ":https", "server listen address")
	innerFlag = flag.String("inner", ":8080", "internal server address")
	hostFlag  = flag.String("host", "127.0.0.1", "server host name")
	certFlag  = flag.String("cert", "", "TLS certificate")
	keyFlag   = flag.String("key", "", "TLS private key")
	debugFlag = flag.Bool("debug", true, "enable debug mode")

	usernameFlag = flag.String("username", "", "username for basic auth")
	passwordFlag = flag.String("password", "", "password for basic auth")
)

func logInit() {
	if *debugFlag {
		log.SetFlags(log.LstdFlags | log.Lshortfile | log.Lmsgprefix)
		log.SetPrefix("[debug]")
	}
}

func main() {
	flag.Parse() // CLI parse
	logInit()    // log innitial

	go internalServerRun()
	publicServerRun() // start server
}
