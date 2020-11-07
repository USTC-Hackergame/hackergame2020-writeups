# 小桂的 wwwwwwwriteup (?

<br>

### 先说说小桂的背景w

> 这是第一次参加 CTF 比赛w！

小桂擅长的是实用编程啦，所以解的大部分都是可以盲目的写代码就能解决的题嗯w\
（论一个对数理，密码学，二进制逆向全都不感兴趣的高四留学生怎样拿的 #18 (╯‵□′)╯︵┻━┻\
然后就是这里只写了感兴趣的嗯，大家答案都一样的那种就不写啦w

虽然代码写的真的很长也发出来啦，大部分都是用 Kotlin 解的嗯w\
（第一次参赛不知道 Python 有那么多方便的 CTF 库就写了好多轮子 /-\

<br>

## 来自未来的 ~~D-Mail~~

（会有 3020 的考古队看到这个嘛w？:thinking:

1. 把 QR **解析**成 `byte[]` 然后写到文件里（和 rawBytes 不一样哦！
2. 用 tar 解开那个文件w
3. 用 tar 解开 `repo.tar.xz`

### 过程

这道题真的饶了好大一圈哇w\
Python 的库试过的: zbar 装不上，qrtools 不能用来解析，pyzbar 很多都是空的 ;-;\
然后用了 Java 的 ZXing 啦w\
（btw 默认配置会报错找不到 QR 码在图中的哪里（还能在哪里呀 (╯‵□′)╯︵┻━┻\
但是配置好之后 `rawBytes` 加在一起却不能被压缩格式读出来...

当时已经快要放弃了的时候发现 `rawBytes` 和解析出来的字符串的 HEX 对应不上！\
然后才发现 `rawBytes` 是 QR 码读出来的未处理格式啦w\
但是 ZXing 库也不会存没有被 String encode 的解析数据，那怎么办呢w\
啊哈哈哈最后直接改了 ZXing 的源码把 `byte[]` 转换成字符串的地方加进去了

```diff
*** com.google.zxing.qrcode.decoder.DecodedBitStreamParser
@@ -232,235 +234,241 @@
    readBytes[i] = (byte) bits.readBits(8);
  }

+ // CTF: Append the parsed bytes
+ CTFQRKt.setParsedBytes(Bytes.concat(CTFQRKt.getParsedBytes(), readBytes));

  String encoding;
  if (currentCharacterSetECI == null) {
```


