# Writeup

这里主要就写下部分题目跟官方不太一样的解法或者步骤，和一些额外的有用的工具。

## 超简单的世界模拟器

[Play John Conway's Game of Life](https://playgameoflife.com/) 这个网站上的 Lexicon 部分提供了很多好用的 "gadget"，翻了一下找到了 [acorn](https://playgameoflife.com/lexicon/acorn)，把这个摆在合适的位置就可以清除两个目标了。

## 自复读的复读机

> 你也可以通过读取当前进程的内存来找到自己的源代码然后输出，理论上完全可行，但我没有实现，如果有选手做到了可以提 PR 来分享给大家。

既然官方 writeup 都这么说了我就来分享一下，我就是这么搞的。

我是每次写 quine 都很头痛的那种人，最开始查了一波，勉强查到了个 reverse quine，但是硬是没想出来怎么弄哈希复读。（要真是 print 常量字符串，那不就要自己子串包含自己哈希？这是极难的吧？）然后就开始绞尽脑汁想如何“开挂”，跟出题人对抗。既然是开挂那就是要违背 quine 的精神，能想到下面几种思路：

- 拿 shell 直接拿 flag
- 通过外部载入代码或者临时文件保存信息（第二次连接读取第一次写入的临时文件）
- 设法去读取到输入的代码（而不是通过构造巧妙的 quine 结构来“自产生”）

很容易拿到 shell，上去逛了一圈没看到 flag。看到了源码，发现是降权执行的输入的代码，通过管道把输入的代码传入一个 `exec(input())` 的 Python 脚本来执行，并且检查输出。flag 只有 root 权限可读。这就意味着我们必须通过输出符合条件的东西来拿 flag，拿 shell 是没用的。

想通过网络载入更多代码，发现禁止了出站网络连接。想通过 stdin 继续输入更多的内容，然而是管道，不太行。试图写入临时文件，发现 `/tmp` 和 `/var/tmp` 目录被 mount 成了只读（可能出题人已经想到了有人会想去写临时文件？）`/dev/shm` 目录可写，但是第一次连接写入的文件在第二次连接就没了（想起来[去年的知乎问题上某出题人写道](https://www.zhihu.com/question/351947330/answer/866177844)，每次连接是新开的 Docker 容器）。所以现在能考虑的方式就只有“设法读取到输入的代码”了。

由于题目的结构，使用 `__file__` 毫无价值。尝试读取 `/proc/self/fd/0`, `/dev/tty` 等等的文件，没有用（输入是管道应该是不能 seek，非交互式运行没有 tty）。最后只能想到一条路了：从内存里面强行扒出输入的代码。代码必然在内存里面，这样肯定行。

按照我对 Python 的研究，想要在 Python 里面直接获得底层（C 语言级别）读取内存的能力，有以下三种方法：

- 使用 ctypes 库
- 在 Linux 上使用 `/proc/self/mem` 文件
- pwn 掉 Python
  - 使用一个存在了多年的字节码攻击，被官方认为是 won't fix （详见[我在 0CTF 2020 里面出的题目的 writeup](https://github.com/gousaiyang/my-ctf-challenges/tree/master/PyAuCalc)）
  - 其他任何可能的底层漏洞

反正这道题目根本没有防御读取内存的方法，那就随便选一个。`/proc/self/mem` 写起来比较简单。

用 gdb-peda 调试 Python，执行 `exec(input())`，可以发现输入的代码存在于堆中。

可以写出以下 exp（以反向复读为例）：

```python
123456,exec("import re\n\nwith open('/proc/self/maps', 'r') as f:\n    for line in f:\n        if '[heap]' in line:\n            start, end = line.split()[0].split('-')\n            start = int(start, 16)\n            end = int(end, 16)\n            break\nwith open('/proc/self/mem', 'rb') as f:\n    f.seek(start)\n    data = f.read(end - start)\n\nresult = sorted(set(x for x in re.findall(br'123456.*?6\\x354321', data) if len(x) > 100))\nprint(result[0].decode()[::-1],end='')\n"),654321
```

这个 payload 是包成一行方便提交的，中间的 `exec` 部分展开来是：

```python
import re

with open('/proc/self/maps', 'r') as f:
    for line in f:
        if '[heap]' in line:
            start, end = line.split()[0].split('-')
            start = int(start, 16)
            end = int(end, 16)
            break
with open('/proc/self/mem', 'rb') as f:
    f.seek(start)
    data = f.read(end - start)

result = sorted(set(x for x in re.findall(br'123456.*?6\x354321', data) if len(x) > 100))
print(result[0].decode(),end='')  # change this line to do reverse or sha256
```

解析 `/proc/self/maps` 找到堆段地址范围，然后暴力全部读出来，匹配特征位点从而精准切割出输入的代码（payload 开头和结尾特意放了 `123456` 和 `654321` 来方便定位），然后对代码做任何想做的操作。嗯，开挂成功了。

后来发现哈希复读做出来的人怎么这么多，难道都会扒内存？或者掌握了子串包含自己哈希的绝技？后来查到了 `exec(s:='print("exec(s:=%r)"%s)')`，这个是很好用的框架，很容易改出反向和哈希等等不同的需求，怪不得这么多人做出来。

P.S. 出题人如果想要禁掉读内存的做法的话，得加 seccomp 白名单少量 syscall（不让 open），再加 [audit hook](https://www.python.org/dev/peps/pep-0578/) 来禁掉 ctypes 和其他 Python 级别的敏感操作。

## 233 同学的 Docker

用 [dive](https://github.com/wagoodman/dive) 工具查看层之后，可以直接去 `/var/lib/docker/overlay2/` 这个目录下面去 find/grep 找 flag。

## 从零开始的 HTTP 链接

很多工具（比如 nc）不支持 0 号端口，它们直接认为输入 0 号端口是一种错误。然后发现 Python 内置的 socket 库可以连接 0 号端口（在 Linux 服务器上试验可以，本地 Windows 不成功，可能是系统或者硬件等等问题）。

连接上去之后手动发送 HTTP 请求，返回的 HTML 里面跟网页终端一样的，又是要让我连接 WebSocket。我当然想搞个代理转发啊（然后用浏览器），但是感觉不太好搞，索性继续找自动化 WebSocket 连接的库。

找到了 [websocket-client](https://github.com/websocket-client/websocket-client)，看起来还不错，但是它也不支持 0 号端口。不过既然底层还是会调用 Python 内置的 socket 库，我们只需要 patch 一下 websocket-client 的代码对端口处理的部分就可以了（Python 代码本来也好改，比改 nc 源码重新编译还是要方便多了吧）。

## 超简陋的 OpenGL 小程序

一开始各种魔改 fs 和 vs 文件都不行（我完全不了解图形学）。后来在 1400048E5 地址下断点（这里在调用 `glDrawElements` 函数），把 `rcx` 改成 0，即可不绘制挡住 flag 的矩形。

## 来自未来的信笺

找了很多二维码解析工具，它们对二进制数据支持都不好，都假定数据是文本。[ZXing Decoder Online](https://zxing.org/w/decode.jspx) 能够解析出来（能看到 `api.github.com` 那堆 JSON 数据），但是无法正确地显示不可打印字符。最后找到[这么个网页 API](http://goqr.me/api/doc/read-qr-code/)，二进制数据解析得很正确。

## 超安全的代理服务器

第一步：[h2c](https://github.com/fstab/h2c) 这个工具也可以用来获取 HTTP/2 server push 的内容。

第二步，我没有用 IPv6 地址，而是用了 `http://www.ustc.edu.cn.127.0.0.1.xip.name:8080`（SSRF 经典操作啊）。

## 超精准的宇宙射线模拟器

题目没有开启 Full RELRO，所以也可以把 `exit` 函数的 GOT 表项从 0x401070 改成 0x401170 (一个 `ret` gadget，相当于空函数)，从而恰好让题目的循环继续运行。
