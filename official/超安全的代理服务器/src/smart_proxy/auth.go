package main

import (
	"encoding/base64"
	"log"
	"net/http"
	"strings"
)

func basicAuth(r *http.Request) (username, password string, ok bool) {
	auth := r.Header.Get("Authorization")
	if auth == "" {
		if r.URL.User.Username() != "" {
			user := r.URL.User.Username()
			pass, isPass := r.URL.User.Password()
			if isPass {
				return user, pass, true
			}
			return user, "", true
		}
		return
	}
	return parseBasicAuth(auth)
}

func parseBasicAuth(auth string) (username, password string, ok bool) {
	const prefix = "Basic "
	// Case insensitive prefix match. See Issue 22736.
	if len(auth) < len(prefix) || !strings.EqualFold(auth[:len(prefix)], prefix) {
		return
	}
	c, err := base64.StdEncoding.DecodeString(auth[len(prefix):])
	if err != nil {
		return
	}
	cs := string(c)
	s := strings.IndexByte(cs, ':')
	if s < 0 {
		return
	}
	return cs[:s], cs[s+1:], true
}

func basicAuthHandle(w http.ResponseWriter, req *http.Request) bool {

	if *usernameFlag == "" && *passwordFlag == "" {
		// pass basic auth check
		return true
	}

	username, password, ok := basicAuth(req)
	if !ok {
		w.Header().Set("WWW-Authenticate", `Basic realm="Restricted"`)
		w.WriteHeader(http.StatusUnauthorized)
		return false
	}

	if username == *usernameFlag && password == *passwordFlag {
		return true
	}

	log.Println("invaild username and password:", username, password)
	w.Header().Set("WWW-Authenticate", `Basic realm="Restricted"`)
	w.WriteHeader(http.StatusUnauthorized)
	return false
}
