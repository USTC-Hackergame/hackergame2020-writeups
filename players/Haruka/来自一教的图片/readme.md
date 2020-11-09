# 来自一教的图片

看到图片里面有奇怪的纹理，我第一反应是他是不是个奇怪的 binary 被编码成了黑白图片（事实证明我想太多了），于是快速写了个程序用各种方式转换成二进制：

```py
...
for j in range(600):
    for i in range(600):
        #byte = (byte >> 1) | ((0 if not p[i, j] else 1) << 7)
        byte = (byte << 1) | (1 if not p[i, j] else 0)
        count += 1
        if count == 8:
            data.append(byte)
            byte = 0
            count = 0

open("/tmp/8", "wb").write(data)
```

结果试了各种位序和位翻转都没有得到有意义的图片，甚至试着将原图片转换成其他尺寸也没有得到任何有效结果。

重新审题发现：

> 小 P 在一教做**傅里叶光学**实验时

结果解题方式是藏在题干里的啊！果然需要认真读题。看来这个图片是某个写着 flag 的图片通过 fft 得到的。

窝懒，于是直接找到了一个[在线网站](http://bigwww.epfl.ch/demo/ip/demos/FFT/)来处理图片。虽然这个网站会把 600x600 的图片缩小到 512x512，但足够看清图片上写的 flag 了。