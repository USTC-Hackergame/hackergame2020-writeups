# 来自未来的信笺

下载文件后发现是一大坨二维码，随手一扫发现还都是二进制内容。

于是这道题看来只需要把所有二维码都扫出内容来拼接成文件即可。

首先想用 python 处理，但试用了几个库发现都有问题：zxing 有些文件无法识别，pyzbar 的封装无法正常获取二进制内容（魔改也没能成功魔改出来）。

改了半天代码，就在我想放弃直接写个 c 程序调用 zbar 的时候，突然发现 zbar 其实是提供了 bin 的，叫 `zbarimg`，可以直接在命令行下处理文件。

于是直接写了个一行脚本：

```sh
for i in `ls frames/*.png`; do echo $i; zbarimg --nodbus -q --raw --oneshot -Sbinary $i >> bin; done
```

跑完即可得到 `bin` 文件。之后 `file` 发现是个 tar，解压缩后发现有 `META`，`COMMITS` 和 `repo.tar.xz` 文件，看上去似乎是个 git repo 的打包。于是解压缩 `repo.tar.xz`，发现 flag 文件就在里面。

（从 flag 内容发现原来这道题的灵感来自 GitHub 北极计划的，又读了一遍题才发现里面其实充满了暗示