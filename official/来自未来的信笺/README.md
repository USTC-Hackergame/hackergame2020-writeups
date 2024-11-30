# 来自未来的信笺

- 题目分类：general

- 题目分值：200

你收到了一封邮件。没有标题，奇奇怪怪的发件人，和一份奇怪的附件。日期显示的是 3020 年 10 月 31 日。

"Send from Arctic." 正文就只有这一句话。

「谁搞的恶作剧啊……话说这竟然没有被垃圾邮件过滤器过滤掉？」你一边嘟囔着一边解压了附件——只看到一堆二维码图片。

看起来有点意思。你不禁想试试，能否从其中得到什么有意义的东西。

[打开/下载题目](files/frames.zip)

---

这道题的灵感来源于今年的 GitHub Archive Program: 将代码冰封在北极之中，以供未来的人类了解我们这个时代的计算机与软件技术。这道题目尝试模仿了 [GitHub Code Vault 指南](https://github.com/github/archive-program/blob/master/GUIDE_zh.md)（[英文版](https://github.com/github/archive-program/blob/master/GUIDE.md)）中的描述。但是由于从简单的描述中，我也没有办法 100% 还原备份的方式，所以这道题可能会和实际情况有比较大的差别。

思路其实很简单：解码所有二维码图片，（按照字典序）拼在一起，可以得到一个 `.tar` 文件，然后解压缩，可以得到一个 `repo.tar.xz` 文件，一个 `META` 文件和一个 `COMMITS` 文件（这些文件是按照 [GitHub Code Vault 指南/如何提取档案库的内容/将存档文件解包为其所包含的不同子文件](https://github.com/github/archive-program/blob/master/GUIDE_zh.md#%E5%B0%86%E5%AD%98%E6%A1%A3%E6%96%87%E4%BB%B6%E8%A7%A3%E5%8C%85%E4%B8%BA%E5%85%B6%E6%89%80%E5%8C%85%E5%90%AB%E7%9A%84%E4%B8%8D%E5%90%8C%E5%AD%90%E6%96%87%E4%BB%B6) 中的描述去生成的，虽然有细节不一致的地方，比如说 `COMMITS` 没有被压缩）。然后再解压 `repo.tar.xz` 文件，就能获得 flag 了。

但是压缩包里一共有 351 张二维码图片，一张一张去 decode 显然是不现实的，并且由于二维码直接编码了 raw data，去类似于二维码解码的网站查看二维码的内容也是不可行的（至少我还没有找到网站能处理这样的二维码的）。这个时候我们需要一些方便的工具去解决问题。

这里我们使用 [zbarimg](https://github.com/mchehab/zbar/tree/master) 这个命令行工具去 decode 二维码，于是这个问题就可以通过写一个小 shell 脚本去解决了。（假设 frames.zip 在工作目录的上一层目录）

```shell
#!/bin/sh

unzip ../frames.zip
[ -e repo.tar ] && rm repo.tar
touch repo.tar

for i in frame-*.png; do
echo "$i"
# https://stackoverflow.com/questions/60506222/encode-decode-binary-data-in-a-qr-code-using-qrencode-and-zbarimg-in-bash
# requires zbar >= 0.23.1
zbarimg --raw -q -Sbinary "$i" >> repo.tar
done;

tar -xf repo.tar
```

如果一切正常，那么 decode 出来就会是一个 tar 文件。解压缩获取 repo.tar.xz 之后再解压缩，就是 flag 了。

## 关于 ZBar 的一个坑

在 ZBar 的 0.23.1 版本之前，当解码包含二进制数据的二维码时，它会尝试去猜测数据的编码，从而可能解码出错误的结果。详见 <https://stackoverflow.com/questions/60506222/encode-decode-binary-data-in-a-qr-code-using-qrencode-and-zbarimg-in-bash>。

另外一句题外话是，在写 writeup 的时候我也听说做这道题的选手们试了各种各样的二维码 decoding 的库，但是很多都没法完全正常工作——我开始有点担心一千年之后的人类能不能正确解码胶卷上的二维码了。

## 关于生成的二维码的细节

以下内容参考了 <https://en.wikipedia.org/wiki/QR_code#Design>。

可能有很多同学还是第一次见到这种密密麻麻~~到会让密集恐惧症患者不满~~的二维码。因为我们编码的文件比较大，在生成二维码的时候，我希望一张图片中可以包含尽可能多的内容，所以我选择了：

- Version 40（177x177）
- Level L (Low) 的错误纠正等级，此时 7% 的数据可以被恢复。因为分发的是完整高清的图片，不会存在扫描出错的问题，所以尽可能地减小了错误纠正码占总数据的比重。

如果用 40-L 编码二进制数据，一张二维码中可以存放 2953 个 bytes。不过有趣的一点是，对于特定的数据，二维码可以存储更多的内容，例如对于 40-L 格式来说，它能够存储 7089 个数字，4296 个 alphanumeric（包括数字、大写字母、空格，以及其他一些字符），1817 个日文汉字（Kanji，每个字符 13 bit）。

最终的二维码使用 `qrencode` 生成。