package main

import (
	"errors"
	"fmt"
	"html/template"
	"log"
	"net"
	"net/http"
	"strings"
	"time"
)

func proxyErrorHandle(w http.ResponseWriter, req *http.Request, code int, err error) {
	tmpl, _ := template.New("index").Parse(tmplStr)
	msg := tplMsg{}
	if err != nil {
		if *debugFlag {
			log.Println("[proxy]", err)
		}
		msg.Err = template.HTML(err.Error())
	}
	w.WriteHeader(code)
	tmpl.Execute(w, msg)
}

func proxyHandle(w http.ResponseWriter, req *http.Request) {

	hostPort := req.URL.Host
	if hostPort == "" {
		hostPort = req.Host
	}
	host, port, err := net.SplitHostPort(hostPort)
	if err != nil {
		err = errors.New("[proxy] HTTP 代理请求格式错误")
		proxyErrorHandle(w, req, http.StatusBadGateway, err)
		return
	}

	secrestReq := req.Header.Get("Secret")
	if secrestReq != secretText {
		err = errors.New("[proxy] Secret 不正确")
		proxyErrorHandle(w, req, http.StatusForbidden, err)
		return
	}

	// Allow List check
	ret := aclCheck(host, port)
	if ret != true {
		err = fmt.Errorf("[proxy] 代理请求 %v:%v 不被访问控制列表所允许", host, port)
		proxyErrorHandle(w, req, http.StatusForbidden, err)
		return
	}

	// outbound
	outbound, err := net.DialTimeout("tcp", hostPort, 10*time.Second)
	if err != nil {
		err = errors.New("[gateway] 无法建立到 " + hostPort + " 的连接")
		proxyErrorHandle(w, req, 502, err)
		return
	}
	defer outbound.Close()

	// // Return 200
	wFlusher, ok := w.(http.Flusher)
	if !ok {
		err = errors.New("[gateway] flusher 不被支持! 请联系比赛组织方。错误码 0x03")
		proxyErrorHandle(w, req, 500, err)
		return
	}

	switch req.ProtoMajor {
	case 1:
		hijacker, ok := w.(http.Hijacker)
		if !ok {
			proxyErrorHandle(w, req, http.StatusInternalServerError, errors.New("内部错误，请联系比赛组织方！错误码 0x01"))
			return
		}
		clientConn, bufReader, err := hijacker.Hijack()
		if err != nil {
			proxyErrorHandle(w, req, http.StatusInternalServerError, errors.New("内部错误，请联系比赛组织方！错误码 0x02"))
			return
		}
		defer clientConn.Close()

		if bufReader != nil {
			// snippet borrowed from `proxy` plugin
			if n := bufReader.Reader.Buffered(); n > 0 {
				rbuf, err := bufReader.Reader.Peek(n)
				if err != nil {
					proxyErrorHandle(w, req, http.StatusInternalServerError, errors.New("隧道错误"))
					return
				}
				outbound.Write(rbuf)
			}
		}

		res := &http.Response{StatusCode: http.StatusOK,
			Proto:      "HTTP/1.1",
			ProtoMajor: 1,
			ProtoMinor: 1,
			Header:     make(http.Header),
		}
		res.Write(clientConn)

		dualStream(outbound, clientConn, clientConn)
	case 2:
		defer req.Body.Close()
		w.WriteHeader(200)
		wFlusher.Flush()
		dualStream(outbound, req.Body, w)
	default:
		proxyErrorHandle(w, req, http.StatusHTTPVersionNotSupported, errors.New(" HTTP 协议版本出错"))
	}
}

var wl = []string{"ustc.edu.cn", "www.ustc.edu.cn"}

func aclCheck(host, port string) bool {

	// _, inport, err := net.SplitHostPort(*innerFlag)
	// if err != nil {
	// 	inport = "8080"
	// }

	// if port != "80" && port != "443" && port != inport {
	// 	log.Println(1)
	// 	return false
	// }

	for _, w := range wl {
		if strings.Contains(host, w) {
			return true
		}
	}

	ip := net.ParseIP(host)
	log.Println(ip)
	if ip != nil {
		if ip.IsGlobalUnicast() {
			return false
		}
		if ip4 := ip.To4(); ip4 != nil {
			if ip4[0] == 192 && ip4[1] == 168 {
				return false
			}
			if ip4[0] == 127 || ip4[0] == 10 || ip4[0] == 172 {
				return false
			}
		}
		return true
	}
	return false
}
