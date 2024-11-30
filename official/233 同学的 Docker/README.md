# 233 同学的 Docker

- 题目分类：general

- 题目分值：150

233 同学在软工课上学到了 Docker 这种方便的东西，于是给自己的字符串工具项目写了一个 Dockerfile。

但是 233 同学突然发现它不小心把一个私密文件（`flag.txt`）打包进去了，于是写了一行命令删掉这个文件。

「既然已经删掉了，应该不会被人找出来吧？」233 想道。

- Docker Hub 地址：[8b8d3c8324c7/stringtool](https://hub.docker.com/r/8b8d3c8324c7/stringtool)

---

[这道题的 Dockerfile](./src/Dockerfile)

## 命题背景与思路

Docker 可能是目前最流行的容器管理器，但很多人（包括一些培训机构）并没有理解 `RUN` 的真正功能，而是把 Dockerfile 当 shell 脚本去写，最后了生成巨大的镜像。这道题提示大家，垃圾文件没删事小，泄漏隐私事大。一定要合理使用 `RUN`！

## 解法

对于没有了解过 Docker 的同学来说，此时从头学起也不晚。如果你看的是质量过硬的资料，它应该会告诉你，每条 `RUN` 命令将产生一个新的 layer，旧 layer 将被保留下来。此时题设中的

> 于是写了一行命令删掉这个文件

应该会提示到你：233 同学用的应该正是诸如 `RUN rm flag.txt` 这样的命令。结合上面所说的 “旧 layer 被保留”，应该是有办法把某个 layer 中的文件取出来的。于是，接下来的思路就是：找到这个 layer，找到这个文件。

既然有思路了，就可以着手解题了。第一步当然是把镜像拉下来。

```
docker pull 8b8d3c8324c7/stringtool
```

这里的 Dockerfile 因为是从真实项目中复制的，所以大小也非常真实，请耐心等待。

### Docker 镜像分析

有诸多手段可以供大家使用。

1. 直接在 Docker Hub 的 [Image Layers](https://hub.docker.com/layers/8b8d3c8324c7/stringtool/latest/images/sha256-aef87a00ad7a4e240e4b475ea265d3818c694034c26ec227d8d4f445f3d93152?context=repo) 页面上看。
2. 使用 [`dive`](https://github.com/wagoodman/dive)。
3. 使用 `docker inspect` 之类的命令。

最终可以确认到 flag 应该在 `/code/flag.txt` 中。

### 提取文件

这里也有诸多手段。一种简单且所有系统通用的方法是使用 `docker save`，下面仅介绍这种方法。

```
docker save 8b8d3c8324c7/stringtool > img.tar
mkdir img
tar xvf img.tar -C img
```

至于之后是怎么确定文件在哪里，就各凭本事了。比如 grep，比如暴力展开所有 tar。实际上可以直接去看 manifest.json，倒数第二个就是倒数第二层（文件到底在哪一层可以通过上一步分析得出）。

```
cd c319bce601a5672aa9ff8297cfde8f65479a58857c1da43f6cd764df62116d9d
tar xvf layer.tar
cat code/flag.txt
```

这时就会输出我们想要的 flag：

```
flag{Docker_Layers!=PS_Layers_hhh}
```
