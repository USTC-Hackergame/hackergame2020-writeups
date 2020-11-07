记录我的一些和官方题解可能不太一样的思路以及一些代码。

---

第4题：一闪而过的flag
---------------------

很简单的题，熟悉命令行的用户肯定知道直接在命令行用shell（cmd 或 powershell 或 unix shell 等）执行就可以了，不必要拖拽之类的鼠标操作。

提这道题主要是提一句关于wine的事情，在[ArchWiki的wine条目](https://wiki.archlinux.org/index.php/Wine#Tips_and_tricks)以及[WineHQ官网的User's Guide页面](https://wiki.winehq.org/Wine_User%27s_Guide#Text_mode_programs_.28CUI:_Console_User_Interface.29)都提及了可以使用`wineconsole`来运行windows命令行程序。虽然我这次没有实际测试过，不过我觉得应该不成问题。

第6题：超简单的世界模拟器
-------------------------

直接说第二问。因为下面那个砖块在地图的右下但更偏右的方向，所以简单的飞行器是不行的，需要能产生复杂演化的初始状态。比如下面这个经典的：

```
110
011
010
```

不过因为题目中的生命游戏显然不是无限大的而是有边界的，所以会稍微有一些区别，需要实际测试。每次移动一点位置，经过数量不太多的测试，我得到了一个解：

```
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000001111
000000000010001
000000000000001
000000000010010
000000000000000
000000000000000
000000001100000
000000000110000
000000000100000
```

关于生命游戏，在网上能搜到很多东西，就不多赘述了，只提两个：
 - [LifeWiki](https://www.conwaylife.com/wiki/Main_Page)，非常详细的wiki站点。
 - [Golly](http://golly.sourceforge.net/)，一个漂亮且功能全面的生命游戏实现，跨平台的自由软件（许可证：GPLv2+）。就在今年10月30日刚发布了4.0新版本。

第7题：从零开始的火星文生活
---------------------------

这道题我真完全没想到只用编码解码就能解决，看题解时还十分惊讶。-_-0 我的思路是从字节构成的规律来解决。

首先，用`GBK`打开文件的话是真的乱码，而用`UTF-8`解码打开文件后可以看到全是汉字，于是从这里入手。仔细看看这些汉字，会发现它们的读音都十分接近，尤其是存在大量声母是"l"的字。如果对gbk(或是gbk2312)有一点了解的话，可能会想起来：gb2312的数千个常用字符在编码中是[按拼音排序](https://zh.wikipedia.org/wiki/GB_2312#%E5%88%86%E5%8C%BA%E8%A1%A8%E7%A4%BA)的，而gbk[几乎完全](https://zh.wikipedia.org/wiki/GB_2312#%E4%B8%A4%E7%A7%8D%E4%B8%8D%E5%90%8C%E7%9A%84GB/T_2312%E5%AE%9E%E7%8E%B0)兼容gbk2312。这一点就意味着，如果把这段文字用gbk编码后，字节之间的数据会非常接近、即：相似度很高，这便提供了一个突破口。

对于从数据中解码信息的问题，通常需要寻找数据中存在的某种“规律”或称“模式”，并以此分析出真正有效的信息。其中，能看到文件第3行（文字的第2行）文字的规律性最为明显：第奇数个汉字全都是“拢”，那么我们基本可以认为这些“拢”字基本上是不提供任何有效的信息的，于是把它们去掉。如果整段文字是符合同一种模式的话，从第2行文字入手解决并推广到整段文字，可能就可以解决问题了。去掉“拢”的第二行如下：

```python shell
>>> s = "忙矛谩莽没脠麓枚鲁脽脝玫脦脽梅卤脭猫脽鲁卯茫掳盲卤卯莽脽麓脦盲脽盲鲁茫掳脛卤卯脟脽鹿帽脛虏脪赂猫贸媒"
```

接着刚才的思路，把它们用`gbk`编码，得到如下字节：

```python shell
>>> b = s.encode("gbk")
>>> b
b'\xc3\xa6\xc3\xac\xc3\xa1\xc3\xa7\xc3\xbb\xc3\x88\xc2\xb4\xc3\xb6\xc2\xb3\xc3\x9f\xc3\x86\xc3\xb5\xc3\x8e\xc3\x9f\xc3\xb7\xc2\xb1\xc3\x94\xc3\xa8\xc3\x9f\xc2\xb3\xc3\xae\xc3\xa3\xc2\xb0\xc3\xa4\xc2\xb1\xc3\xae\xc3\xa7\xc3\x9f\xc2\xb4\xc3\x8e\xc3\xa4\xc3\x9f\xc3\xa4\xc2\xb3\xc3\xa3\xc2\xb0\xc3\x84\xc2\xb1\xc3\xae\xc3\x87\xc3\x9f\xc2\xb9\xc3\xb1\xc3\x84\xc2\xb2\xc3\x92\xc2\xb8\xc3\xa8\xc3\xb3\xc3\xbd'
```

接着观察，发现这些字节中第奇数位置上的字节几乎都是`\xc3`，也有部分`\xc2`，结合gbk中常用汉字“一个汉字两个字节”的事实，我们可以把这个字节串以两字节为一组，展开成二进制形式：

```python shell
>>> def chr2int(c: str) -> int:
...     x, y = c.encode("gbk")
...     return (x << 8) | y
...
>>> l = list(map(chr2int, s))
>>> [bin(i) for i in l]
['0b1100001110100110',
 '0b1100001110101100',
 '0b1100001110100001',
 '0b1100001110100111',
 '0b1100001110111011',
 ...
 '0b1100001110101000',
 '0b1100001110110011',
 '0b1100001110111101']
```

可以看到，大部分位都是完全一样的。用位运算我们可以具体看到哪些位是一直没有变化的：

```python shell
>>> from operator import and_, or_  # 按位与、按位或
>>> from functools import reduce
>>> reduce_and = reduce(and_, l)
>>> reduce_or = reduce(or_, l)
>>> bin(reduce_and)
'0b1100001010000000'
>>> bin(reduce_or)
'0b1100001110111111'
>>> bin(reduce_and ^ reduce_or)
'0b100111111'
```

可以看到，最后得到的这7位就是实际编码数据的bit。7位，ASCII码不正好就是7位吗？于是把这7位解码为ASCII：

```python shell
>>> def dec(c: int) -> int:
...     return ((c & 0b1_00000000) >> 2) | (c & 0b111111)
...
>>> b = bytes(map(dec, l))
>>> b
b'flag{H4v3_FuN_w1Th_3nc0d1ng_4Nd_d3c0D1nG_9qD2R8hs}'
```

惊讶地发现，这就已经是flag了，那么剩下的文字就与我们无关了，提交flag继续下一题吧（逃）

第8题：自复读的复读机
---------------------

经过搜索，找到了知乎上的这一篇文章：[Python输出自身的4种写法](https://zhuanlan.zhihu.com/p/34882073)，于是直接抄过来（

仅仅是文章中的第一种写法就完全足够了，思路很清晰：依靠字符串格式化来递归地构造代码字符串，并进行输出。

```python
quotation = chr(0x22)
newline = chr(0x0a)

s = "quotation = chr(0x22){0}newline = chr(0x0a){0}{0}s = {1}{2}{1}{0}s = s.format(newline, quotation, s){0}{0}print(s)"
s = s.format(newline, quotation, s)

print(s)
```

需要注意的是，为了保持格式化后的字符串与代码自身的一致性，这里不能使用任何形式的转义字符（引号、换行符），所以原作者在这里使用内置函数`chr`来得到这些字符。另外，本题需要代码限制在一行，那么我们使用分号代替换行符（没错！python支持以分号作为语句结束，直到现在的最新版也仍然支持）：

```python
quotation = chr(0x22)
s = "quotation = chr(0x22); s = {0}{1}{0}; s = s.format(newline, quotation, s); print(s, end={0}{0})"
s = s.format(quotation, s)
print(s, end="")
```

这里为了美观我还是用换行*展示*代码，上面的代码实际上应该是：

```python
quotation = chr(0x22); s = "quotation = chr(0x22); s = {0}{1}{0}; s = s.format(quotation, s); print(s, end={0}{0})"; s = s.format(quotation, s); print(s, end="")
```

上面这段代码只是输出自身，但它已经包含了这道题的一切重点了，接下来我们只需要稍加改动就可以得到两个答案：

```python
# 输出反向
quotation = chr(0x22)
s = "quotation = chr(0x22); s = {0}{1}{0}; s = s.format(quotation, s); print({0}{0}.join(reversed(s)), end={0}{0})"
s = s.format(quotation, s)
print("".join(reversed(s)), end="")

# 输出哈希
from hashlib import sha256
quotation = chr(0x22)
s = "from hashlib import sha256; quotation = chr(0x22); s = {0}{1}{0}; s = s.format(quotation, s); print(sha256(s.encode({0}utf-8{0})).hexdigest(), end={0}{0})"
s = s.format(quotation, s)
print(sha256(s.encode("utf-8")).hexdigest(), end="")
```

第9题：233的字符串工具
----------------------

典型的Unicode题。对于第一问，除了官方题解当中说的之外，实际上在Python官方文档也有一份指引：[Python常用指引 - Unicode指南](https://docs.python.org/zh-cn/3/howto/unicode.html)。其中，在[比较字符串](https://docs.python.org/zh-cn/3/howto/unicode.html#comparing-strings)一节提到了一个很有趣的现象：有的字符(码位)在大小写转换之后会变成两个字符(码位)。在Python官方文档的[内置类型 - 文本序列类型str - str.casefold()](https://docs.python.org/zh-cn/3/library/stdtypes.html#str.casefold)中也提到了。

```python shell
>>> c = "ß"
>>> len(c)
1
>>> c.casefold()
'ss'
>>> len(c.casefold())
2
```

所以，也许有一些字符，在转换成大写以后能变为两个字符呢？人不可能是人形自走Unicode数据库，所以我们需要程序来找。根据Unicode标准，Unicode实际上只有从`0`到`0x10ffff`这一百多万个码位，对于程序来说穷举是轻而易举的事情，于是编写如下代码：

```python
for i in range(0x10ffff):
    c = chr(i)
    if c.upper() in "FLAG":
        print(f"{i=}, {c=}, {c.upper()=}")
```

运行，得到了如下输出：

```
i=65, c='A', c.upper()='A'
i=70, c='F', c.upper()='F'
i=71, c='G', c.upper()='G'
i=76, c='L', c.upper()='L'
i=97, c='a', c.upper()='A'
i=102, c='f', c.upper()='F'
i=103, c='g', c.upper()='G'
i=108, c='l', c.upper()='L'
i=64258, c='ﬂ', c.upper()='FL'
```

OK，搞定。

再看下一问，也很明确，是关于UTF-7的。经过查询wikipedia，跟着这个[示例](https://zh.wikipedia.org/wiki/UTF-7#%E7%AF%84%E4%BE%8B)，可以轻易构造出不唯一的字符串，下面是我当时构造的，不多赘述了。

```
g:  0    0    6    7
 0b0000_0000_0110_0111
 0b000000_000110_0111 00
    0       6       28
    A       G       c
g -> +AGc-
"fla+AGc-"
```

第16题：狗狗银行
----------------

这题的关键就是要发现四舍五入，只要发现了这一点剩下的就十分简单了，设计流程、用浏览器F12扒api、编写爬虫一气呵成。

值得一提的是性能问题，由于这道题涉及大量网络请求，所以如果不进行优化的话运行会很慢。对于爬虫的一个最简单的提升性能方法就是多线程，我这里使用的是Python标准库`concurent.futures`的线程池，非常方便。这里贴一个去掉了调试日志和错误检查的简化版的代码，我做题时的原始代码在[文件](16_狗狗银行.py)里。

```python
from functools import partial
from urllib.parse import urljoin
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

import requests

class DogBankAPI:

    url = "http://202.38.93.111:10100/"
    headers = {"Authorization": ""}

    def reset(self):
        url = urljoin(self.url, "api/reset")
        r = requests.post(url, headers=self.headers)

    def user(self) -> dict:
        url = urljoin(self.url, "api/user")
        r = requests.get(url, headers=self.headers)
        return r.json()

    def create(self, type_: str):
        url = urljoin(self.url, "api/create")
        json_ = {"type": type_}
        r = requests.post(url, headers=self.headers, json=json_)

    def eat(self, account: int):
        url = urljoin(self.url, "api/eat")
        json_ = {"account": account}
        r = requests.post(url, headers=self.headers, json=json_)

    def transfer(self, src: int, dst: int, amount: int):
        url = urljoin(self.url, "api/transfer")
        json_ = {
            "src": src,
            "dst": dst,
            "amount": amount,
        }
        r = requests.post(url, headers=self.headers, json=json_)

def firstday(d: DogBankAPI, executor: ThreadPoolExecutor):
    d.reset()
    def create_credit(i):
        d.create("credit")
        d.transfer(src=i, dst=1, amount=2099)
    def create_debit(i):
        d.create("debit")
        d.transfer(src=1, dst=i, amount=167)
    map = executor.map
    map(create_credit, range(2, 12))
    map(create_debit, range(12, 143))
    d.eat(1)

def otherday(d: DogBankAPI, executor: ThreadPoolExecutor):
    user = d.user()
    if user["flag"] is not None:
        return user["flag"]
    map = executor.map
    map(lambda src: d.transfer(src, (src+8)//10, amount=1), range(12, 112))
    map(lambda src: d.transfer(src, 1, amount=1), range(112, 143))
    d.eat(1)

def main():
    d = DogBankAPI()
    with ThreadPoolExecutor(20) as executor:
        firstday(d, executor)
        flag = None
        while not flag:
            flag = otherday(d, executor)
    print(flag)

main()
```
