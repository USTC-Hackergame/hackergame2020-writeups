package main

import "html/template"

const (
	tmplStr = `<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Smart Proxy!</title>
</head>

<body>
	<center><h1>Smart Proxy!</h1></center>
	<hr>
	{{with .Err}}
	<p style="color:red;">Error: {{.}}</p>
	{{end}}
	{{with .Msg}}
	<p style="color:blue;">Notice: {{.}}</p>
	{{end}}

	{{.Body}}

	<hr style="margin-top: 50px">
	<footer>
	<p>Serve with honor. Smart Proxy, 2020.</p>
	<a href="/">主页</a>
	<a href="/help">帮助</a>
	<a href="http://127.0.0.1{{.Inner}}" referrerpolicy="origin">管理中心</a>
	</footer>
</body>
</html>
`

	indexStr = `<p>我们提供了一个代理服务器，用于访问科大主页（ www.ustc.edu.cn ）。只有拥有 <strong>secret</strong> 的人才是我们尊贵的客人，才能访问我们的服务。 </p>
<p>为了获取更多帮助, 你可以访问 <a href="/help">帮助中心</a> </p>
<p style="display: none"> 一周工作 72 小时的美工上周住进了 ICU，界面难看也先凑合着用吧 </p>`

	helpStr = `	<p> Smart Proxy 是一个基于 HTTP2 协议的超级代理服务器。</p>
<p> 1. 我们的服务只提供基于 <strong>CONNECT</strong> 的代理（欲知详情，请访问 <a href="https://tools.ietf.org/html/rfc7231#section-4.3.6">RFC 7231</a>） </p>
<p> 2. 另外，你需要在你的 HTTP 请求头标中加入 <strong>Secret</strong> 来作为身份凭证, 例如:</p>
<code>
Secret: [your secret here]
</code>
<p> 请注意 <strong>Secret</strong> 只有 60 秒有效期。</p>
<p> 3. 我们使用一个访问控制列表来检查您的访问请求。只有匹配如下域名的请求，才会被代理：</p>

<ul>
<li>ustc.edu.cn</li>
<li>www.ustc.edu.cn</li>
</ul>

在黑名单中的 IP 是无法被代理的:
<ul>
<li>全球单播地址</li>
<li>10.0.0.0/8</li>
<li>127.0.0.0/8</li>
<li>172.16.0.0/12</li>
<li>192.168.0.0/16</li>
</ul>
`

	adminStr = `<!DOCTYPE html>
	<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<title>Smart Proxy!</title>
	</head>
	<body>
		<p>无法连接到管理中心: <strong>http://127.0.0.1:8080</strong> 无法从公网被访问。</p>
	</body>
	</html>
`

	adminErrorStr      = "无法连接到管理中心: <strong>http://127.0.0.1:8080</strong> 无法从公网被访问。"
	versionErrorStr    = "为了更好的提供服务器, 请使用最新的 <strong>HTTP2</strong> 协议。"
	pushErrorStr       = "我们无法向您 <strong>推送（PUSH）</strong> 最新的 <strong>Secret</strong>. 请使用如下浏览器以便于我们给你推送一些消息： Chrome, Firefox, Safari, Microsoft Edge."
	pushSuccStr        = "我们已经向您 <strong>推送（PUSH）</strong> 了最新的 <strong>Secret</strong> ，但是你可能无法直接看到它。"
	maxRequestErrorStr = "别太快了！您已经达到了允许连接的上限了"
)

type tplMsg struct {
	Err   template.HTML
	Msg   template.HTML
	Body  template.HTML
	Inner template.HTML
}
