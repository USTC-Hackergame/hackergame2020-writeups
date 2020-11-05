package main

import (
	"html/template"
	"log"
	"net"
	"net/http"

	"golang.org/x/crypto/acme/autocert"
)

type proxyServer struct{}

func (s *proxyServer) ServeHTTP(w http.ResponseWriter, req *http.Request) {
	indexHandle(w, req)
}

func publicServerRun() {

	go flashUUID()

	poolInit()
	log.Printf("[server] listen to: %v sni:%v", *addrFlag, *hostFlag)

	var err error
	s := &http.Server{
		Addr:    *addrFlag,
		Handler: &proxyServer{},
	}

	if *certFlag == "" || *keyFlag == "" {
		m := &autocert.Manager{
			Cache:      autocert.DirCache("cert"),
			Prompt:     autocert.AcceptTOS,
			HostPolicy: autocert.HostWhitelist(*hostFlag),
		}
		s.TLSConfig = m.TLSConfig()
		go http.ListenAndServe(":http", m.HTTPHandler(nil))

		err = s.ListenAndServeTLS("", "")
	} else {
		err = s.ListenAndServeTLS(*certFlag, *keyFlag)
	}

	if err != nil {
		log.Fatalln("[server] start server error: ", err)
	}
}

func indexHandle(w http.ResponseWriter, req *http.Request) {

	// basic auth for check
	if !basicAuthHandle(w, req) {
		return
	}

	tmpl, _ := template.New("index").Parse(tmplStr)
	msg := tplMsg{
		Body:  indexStr,
		Inner: template.HTML(*innerFlag),
	}

	if *debugFlag {
		log.Printf("[client] from:%v Method:%v Host:%v URL:%v\n", req.RemoteAddr, req.Method, req.Host, req.URL)
	}

	// route
	if req.Method == http.MethodConnect {
		// Do not pass limitations
		remoteHost, _, err := net.SplitHostPort(req.RemoteAddr)
		if err != nil {
			remoteHost = req.RemoteAddr
		}
		if !qosCheck(remoteHost) {
			log.Println("[proxy] reached the maximum number of proxy connections.")
			w.WriteHeader(http.StatusTooManyRequests)
			msg.Err = maxRequestErrorStr
			tmpl.Execute(w, msg)
			return
		}
		qosAdd(remoteHost)
		proxyHandle(w, req)
		return
	}

	// protocol check
	if req.ProtoMajor != 2 {
		log.Println("[http2] use HTTP/1.1 or below, quit!")
		w.WriteHeader(http.StatusHTTPVersionNotSupported)
		msg.Err = versionErrorStr
		tmpl.Execute(w, msg)
		return
	}

	switch req.URL.Path {
	case secureURL:
		secureHandle(w, req)
		return
	case "/help":
		helpHandle(w, req)
		return
	case "/admin":
		adminHandle(w, req)
		return
	}
	if req.URL.Path != "" && req.URL.Path != "/" {
		notFoundHandle(w, req)
		return
	}

	pusher, ok := w.(http.Pusher)
	if !ok {
		log.Println("[http2] Pusher initial error!")
		w.WriteHeader(http.StatusInternalServerError)
		msg.Err = versionErrorStr
		tmpl.Execute(w, msg)
		return
	}

	// Push
	options := &http.PushOptions{
		Header: http.Header{},
	}
	if err := pusher.Push(secureURL, options); err != nil {
		log.Println("Failed to push: ", err)
		w.WriteHeader(http.StatusInternalServerError)
		msg.Err = pushErrorStr
		tmpl.Execute(w, msg)
		return
	}

	msg.Msg = pushSuccStr
	tmpl.Execute(w, msg)
}

func secureHandle(w http.ResponseWriter, req *http.Request) {
	tmpl, _ := template.New("index").Parse(tmplStr)
	msg := tplMsg{}

	rawMsg := "secret: " + secretText + " ! Please use this secret to access our proxy.(flag1: "+flag1+" )"
	msg.Msg = template.HTML(rawMsg)
	tmpl.Execute(w, msg)
}

func helpHandle(w http.ResponseWriter, req *http.Request) {
	tmpl, _ := template.New("help").Parse(tmplStr)
	msg := tplMsg{}
	msg.Body = helpStr
	tmpl.Execute(w, msg)
}

func adminHandle(w http.ResponseWriter, req *http.Request) {
	w.WriteHeader(http.StatusBadGateway)
	w.Write([]byte(adminStr))
}

func notFoundHandle(w http.ResponseWriter, req *http.Request) {
	tmpl, _ := template.New("help").Parse(tmplStr)
	w.WriteHeader(http.StatusNotFound)
	msg := tplMsg{}
	msg.Err = template.HTML("Page Not Found: " + req.URL.Path)
	tmpl.Execute(w, msg)
}
