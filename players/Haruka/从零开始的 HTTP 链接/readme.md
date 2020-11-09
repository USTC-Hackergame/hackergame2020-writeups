# 从零开始的 HTTP 链接

访问 0 端口看来比较麻烦，随手试了几个工具发现基本都不支持。于是想到 scapy 直接构造数据包：

（由于当时是在 ipython 里操作的，因此具体最终命令只能靠命令历史捞，不过大概长这个样子：

```py
from scapy.all import *
syn = IP(dst="202.38.93.111") / TCP(dport=0, flags='S')
syn_ack = sr1(syn)
getStr = 'GET / HTTP/1.1\r\nHost: 202.38.93.111\r\n\r\n'
request = IP(dst="202.38.93.111") / TCP(dport=0, sport=syn_ack[TCP].dport,
            seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr
reply = sr1(request)
```

然后暂时把系统发送的 RST 拦下来（因为 scapy 直接发出去的包系统的协议栈并不认识，收到对应回复就会 RST 回去）：

```
sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -s <local_ip> -j DROP
```

（注：理论上应该用 -d 对端地址，但是窝懒

但抓包发现返回的网页里有这玩意：

```js
      var firstmsg = true;
      const socket = new WebSocket(
        location.origin.replace(/^http/, "ws") + "/shell"
      );
      const attachAddon = new AttachAddon.AttachAddon(socket);
      term.loadAddon(attachAddon);
      socket.onclose = event => {
        term.write("\nConnection closed");
      };
      socket.onmessage = event => {
        if (firstmsg) {
          firstmsg = false;
          let token = new URLSearchParams(window.location.search).get("token");
          window.history.replaceState({}, null, '/');
          if (token) {
            localStorage.setItem('token', token);
          } else {
            token = localStorage.getItem('token');
          }
          if (token) socket.send(token + "\n");
        }
      };
```

哦干，看来还需要连个 ws 还行，那么手工构造一大坨 ws 连接就真的太累了。于是正好刚用完 iptables，就想能不能直接 nat 一下他：

```
# root @ raw in ~ [1:39:19]
$ iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 8881 -j DNAT --to 202.38.93.111:0
iptables v1.6.0: Port `0' not valid

Try `iptables -h' or 'iptables --help' for more information.
```

结果连 DNAT 都不支持 0 端口。

想了想，想用 scapy 来拦截一下流量然后直接改掉包内容，于是搜了搜发现可以使用 iptables NFQUEUE 来拦截包并且可以修改包内容，还找到了一个[现成的 repo](https://github.com/DanNegrea/Scapy-Interceptor) 实现了相关功能。

于是最终用了以下 iptables 项：

```
iptables -A INPUT -s 202.38.93.111 -j NFQUEUE --queue-num 2
iptables -A OUTPUT -d 202.38.93.111 -j NFQUEUE --queue-num 3
```

将发往服务器和从服务器收到的包分别走 NFQUEUE 的 3 号和 2 号队列，然后魔改出来两个 python 程序分别处理两个方向的包（使用的 `netfilterqueue` 库不支持一个程序里同时绑定两个队列，这个地方坑了我一段时间）：

```py
# core logic only
def interrupt_and_edit_out(pkt):
	print("out")
	packet = IP(pkt.get_payload())
	packet[TCP].dport = 0
	del packet[IP].chksum
	del packet[TCP].chksum
	print(repr(packet))
	pkt.set_payload(raw(packet))
	pkt.accept()
	
def interrupt_and_edit_in(pkt):
	print("in")
	packet = IP(pkt.get_payload())
	packet[TCP].sport = 80
	del packet[IP].chksum
	del packet[TCP].chksum
	print(repr(packet))
	pkt.set_payload(raw(packet))
	pkt.accept()
	
```

（完整程序代码：[in.py](in.py), [out.py](out.py)

大概意思就是直接把发出去的包抹成目标端口 0，并且把收到的包抹成来源端口 80，这样直接访问目标服务器的 80 端口即可被转换成访问 0 端口，还不用额外处理内核 TCP 状态问题。

之后直接用 [websocat](https://github.com/vi/websocat) 工具访问 `ws://202.38.93.111/shell`，输入 token 即可获得 flag。