**我是零基础自学的初学者，从今年十一月初开始学的，也就意味着参加比赛之前我几乎没有这方面的经历。**<br>
**百度谷歌都是好帮手，因为我是小白，所以我能做上的题都是可以百度到或者很显然的东西。。。**
*****
# 1 签到
f12步长step改成1

# 2 猫咪问答++
第一个我是确定剩下四个之后穷举的，第二个百度里可以查到，第三题可以百度科大的VR全景，第四题也是百度，第五题也是百度
12，256，9，9，17098

# 3 2048
f12审查代码，找js，搜索fruit，url后面加上/getflxg?my_favorite_fruit=banana

# 4 一闪而过的flag
cmd里运行即可，出flag直接复制粘贴

# 5 从零开始的记账工具人
一千个数据，手搓不慌，然后很可能有输入错误的，所以就用方方格子来把数字转汉语之后两列对比。由于拾圆和壹拾圆格式不太一样，所以还会有两百多不一样但是本质相同的。注意审查即可

# 6 超简单的世界模拟器
蝴蝶效应用图示的飞船模型即可
一石二鸟用图示的右五连模型，而且需要翻转一周
这两个模型在百度上都搜得到

# 7 从零开始的火星文生活
转换ANSI，然后百度乱码恢复

# 8 自复读的复读机
python代码，不解释
```python
s='s=%r;print((s%%s)[::-1],end="")';print((s%s)[::-1],end="")
```
```python
import hashlib;s='import hashlib;s=%r;print(hashlib.sha256((s%%s).encode()).hexdigest(),end="")';print(hashlib.sha256((s%s).encode()).hexdigest(),end="")
```

# 12 来自一教的图片
傅里叶光学，就很好想了。代码如下：
```mathematica
a = Import["_the picture_"] // ImageData
b = Fourier[a]
Abs[b] // Image
```
