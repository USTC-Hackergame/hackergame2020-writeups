package main

import (
	"log"
	"net"
	"net/http"
	"strings"
)

const (
	internalListenAddr = ":8080"
	internalLocalHost  = "127.0.0.1"
)

var (
	internalPublicError   = []byte("管理中心无法从公网直接访问")
	internalFromError     = []byte("管理中心需要从 '" + *hostFlag + "' 被访问(Referer)")
	internalMethodError   = []byte("管理中心不允许该 HTTP 方法（Method)")
	internalNotFoundError = []byte("无法找到请求的页面")
	internnalTokenError   = []byte("Missing 'token': you must 'GET' your flag with your Hackergame Token")
)

type internalServer struct{}

func (s *internalServer) ServeHTTP(w http.ResponseWriter, req *http.Request) {
	remoteHost, _, err := net.SplitHostPort(req.RemoteAddr)
	if err != nil {
		remoteHost = req.RemoteAddr
	}

	if *debugFlag {
		log.Println("[internal] request from", remoteHost, "to", req.Method, req.URL)
	}

	if remoteHost != "localhost" && remoteHost != "127.0.0.1" && remoteHost != "::1" {
		w.WriteHeader(http.StatusForbidden)
		w.Write(internalPublicError)
		return
	}

	referer := req.Header.Get("Referer")
	if !strings.Contains(referer, *hostFlag) {
		w.WriteHeader(http.StatusForbidden)
		w.Write([]byte("管理中心需要从 '" + *hostFlag + "' 被访问(Referer)"))
		return
	}

	if req.Method != http.MethodGet {
		w.WriteHeader(http.StatusMethodNotAllowed)
		w.Write(internalMethodError)
		return
	}

	if req.URL.Path != "/" {
		w.WriteHeader(http.StatusNotFound)
		w.Write(internalNotFoundError)
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("flag2: "+flag2))

	// v := req.URL.Query()
	// token := v.Get("token")
	// if token == "" {
	// 	w.WriteHeader(http.StatusOK)
	// 	w.Write(internnalTokenError)
	// 	return
	// }
	// w.WriteHeader(http.StatusOK)
	// w.Write(getFlag(token))
}

func internalServerRun() {
	addr := *innerFlag
	if addr == "" {
		addr = internalListenAddr
	}
	log.Println("[server] internal  server  listen at", addr)
	err := http.ListenAndServe(addr, &internalServer{})
	if err != nil {
		log.Fatalln("[server] internal server error: ", err)
	}
}

func getFlag(token string) []byte {

	return []byte(flag2)
	// h := md5.New()
	// mT := h.Sum([]byte(token))

	// dst := make([]byte, hex.EncodedLen(len(mT)))
	// hex.Encode(dst, mT)

	// flag := "flag{http_is_amazing_" + string(dst[:5]) + string(dst[len(dst)-5:]) + "}"
	// return []byte(flag)
}
