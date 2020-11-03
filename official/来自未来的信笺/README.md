# 来自未来的信笺

这道题的灵感来源于今年的 GitHub Archive Program: 将代码冰封在北极之中，以供未来的人类了解我们这个时代的计算机与软件技术。这道题目尝试模仿了 [GitHub Code Vault 指南](https://github.com/github/archive-program/blob/master/GUIDE_zh.md)（[英文版](https://github.com/github/archive-program/blob/master/GUIDE.md)）中的描述。但是由于从简单的描述中，我也没有办法 100% 还原备份的方式，所以这道题可能会和实际情况有比较大的差别。

思路其实很简单：解码所有二维码图片，（按照字典序）拼在一起，可以得到一个 `.tar` 文件，然后解压缩，可以得到一个 `repo.tar.xz` 文件，一个 `META` 文件和一个 `COMMITS` 文件（这些文件是按照 [GitHub Code Vault 指南/如何提取档案库的内容/将存档文件解包为其所包含的不同子文件](https://github.com/github/archive-program/blob/master/GUIDE_zh.md#%E5%B0%86%E5%AD%98%E6%A1%A3%E6%96%87%E4%BB%B6%E8%A7%A3%E5%8C%85%E4%B8%BA%E5%85%B6%E6%89%80%E5%8C%85%E5%90%AB%E7%9A%84%E4%B8%8D%E5%90%8C%E5%AD%90%E6%96%87%E4%BB%B6) 中的描述去生成的，虽然有细节不一致的地方，比如说 `COMMITS` 没有被压缩）。然后再解压 `repo.tar.xz` 文件，就能获得 flag 了。

但是压缩包里一共有 351 张二维码图片，一张一张去 decode 显然是不现实的，并且由于二维码直接编码了 raw data，去类似于二维码解码的网站查看二维码的内容也是不可行的。这个时候我们需要一些方便的工具去解决问题。

这里我们使用 [zbarimg](https://github.com/mchehab/zbar/tree/master) 这个命令行工具去 decode 二维码，于是这个问题就可以通过写一个小 shell 脚本去解决了。

[TBD]