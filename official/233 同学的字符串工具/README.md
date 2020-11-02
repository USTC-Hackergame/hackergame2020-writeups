# 233 同学的字符串工具

[这道题的源代码 string_tool.py](./string_tool.py)

## 命题背景与思路

这两道题主要目的是科普与 Unicode 相关的一些知识。目前 Unicode 字符集及其相关的 UTF-8 等编码在互联网上得到了广泛应用，但很多开发者仍然对 Unicode 及其编码的一些「坑点」缺乏认知，如认为 UTF-16 是定长的，认为 UCS-4 中一个码位就是一个字符，没有充分考虑到正则化和 Unicode 的国际化特征等等。

本题两问均有实际背景。

## 「字符串大写工具」题解

这道题的背景见 [Hacking Github with Unicode](https://eng.getwisdom.io/hacking-github-with-unicode-dotless-i/)。

代码的意思是：如果我们输入一个字面上不是 "flag" 但转换为大写后会变成 "FLAG" 的字符串，就可以得到 flag。

我们可以以 "unicode uppercase collision" 为关键字搜索，不难找到一个连字（ligature）

```
ﬂ (0xFB02)
```

这个“字符”将在转换为大写时变成 `FL` 两个字符！因此，只需输入 `ﬂag` 即可得到 flag。

```
flag{badunic0debadbad}
```

## 「UTF-7 转换工具」题解

这道题的背景见 [remove UTF-7 from browser encoding menus](https://bugzilla.mozilla.org/show_bug.cgi?id=441876)。

代码的意思是：如果我们输入一个字面上不是 "flag" 但从 UTF-7 转换为 UTF-8 后会变成 "flag" 的字符串，就可以得到 flag。

不妨查阅 UTF-7 相关资料。可以得知：一个 Unicode 字符串，在 UTF-7 编码下，可能有多种编码，甚至纯粹的 ASCII 字符串也可以有多种编码！

那么事情就简单了。我们依照 Wikipedia 等参考资料给出的 UTF-7 编码算法，可以构造出 "flag" 的另一种“写法”。比如，选择 `f` 下手。

1. `f` 的 Unicode 码位是 0x66
2. 将 0x66 写成 16 位二进制数：`0000 0000 0110 0110`
3. 重新分组：`000000 000110 011000`
4. 使用 [base64 的编码表](https://en.wikipedia.org/wiki/Base64#Base64_table)，将每组变成一个字符：`AGY`

那么最终 "flag" 的另一种 UTF-7 替代写法就是 `+AGY-lag`，输入即可得到 flag。

```
flag{please_visit_www.utf8everywhere.org}
```

（是的，你应该去看这个网站！）
