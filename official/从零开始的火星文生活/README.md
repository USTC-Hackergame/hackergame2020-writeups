# 从零开始的火星文生活

出题&解题[源代码](./src/generate_and_solve.py)

## 思路

还原乱码。也许有人见过这张图：

![常见乱码](files/常见乱码.jpg)

如果是还原乱码小能手或者见过上面那张图就不用我多说了。如果没见过，那么 google 一下部分乱码内容（如 “脦脪鹿楼 乱码”）就能发现一些线索了。

## 过程

下载附件之后假如直接用 GBK 打开那就真的是题面里说的“夹杂着日语和数字的火星文”了，恭喜掉进坑，乱码又多了一层（逃

用 UTF-8 打开，看到形如“脦脪鹿楼”的文本，推断是上图中的“古文码”乱码。但是“古文码”明明是“以 GBK 方式读取 UTF-8 编码的中文”造成的，看来“脦脪鹿楼”本来应当是 GBK下看到的结果，却又被存成了 UTF-8。所以第一步是用 GBK 重新编码文本“脦脪鹿楼...”。

然后用 UTF-8 打开，看到形如“ÎÒ¹¥ÆÆÁË”的文本，推断是上图中的“拼音码”乱码。“拼音码”是“以 ISO8859-1 方式读取 GBK 编码的中文”，而现在文本的编码是 UTF-8。所以接下应当用 ISO8859-1 重新编码文本“ÎÒ¹¥ÆÆÁË...”。

然后用 GBK 打开，就能看到可读的汉字和 flag 了。不过这里的 flag 全部是从 ASCII 字符转成的全角字符，不能直接复制使用，可以手动替换成 ASCII 字符或者用其他简便方法变回 ASCII 字符即可。

[源代码](./src/generate_and_solve.py) 中也给出了一个全角->半角的函数。

## 实践

那么具体用什么手段来解题呢？

### 方法一（不写代码）

例如用 VSCode 的“Select Encoding”功能。

步骤（开始时 UTF-8 打开题目附件）：

1. Save with Encoding -> GBK
1. Reopen with Encoding -> UTF-8
1. Save with Encoding -> ISO8859-1
1. Reopen with Encoding -> GBK

（听说 Notepad++ 很方便，蹲一个其他人的 wp）

### 方法二 （写代码）

见 [源代码](./src/generate_and_solve.py) 中的 solve 函数。

```
def solve(message):
    answer=DBC2SBC(message.encode("gbk").decode("UTF-8").encode("iso-8859-1").decode('gbk'))
    return answer
```

## 为什么出这道题

TBC

没事别 GBK，全盘 UTF-8 不香吗:D