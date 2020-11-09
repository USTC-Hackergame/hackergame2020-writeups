# 动态链接库检查器

随便传了一个文件发现就是打印了一下 ldd 的结果。那么先搜一下 ldd 都有什么洞，很快发现大量来源引用[这篇文章](https://catonmat.net/ldd-arbitrary-code-execution)。

不幸的是，这篇文章中提到的漏洞已经在 2.27 版本中修复，而根据题目信息，服务器使用的版本是 2.28，因此还得找别的漏洞。

（我试了半天文章里的方式，编译 uclibc 还费了半天劲，最后发现在本机都跑不过，读了一下 ldd 代码才发现已经没有那个问题了

于是只能继续搜相关信息，找 ldd cve 的时候找到了[这个 issue](https://sourceware.org/bugzilla/show_bug.cgi?id=22851)。

这个 issue 里提到了一种方式并且给出了完整的实现代码，因此直接照猫画虎搞上一波。然而编译好了以后在本机搞了半天发现只会让本机的 ldd 返回错误，试了半天也没试出结果（本机系统是 Ubuntu 16.04.6，glibc 2.23-0ubuntu11.2, 现在想想大概还是版本问题）。

死马当活马医，按照 issue 里的代码跑出来的文件直接扔给服务器看看好了。

![image](https://user-images.githubusercontent.com/861659/98482689-5db30300-2246-11eb-86e4-89267d8140f5.png)

一阵狂喜，直接改掉 `shellcode.asm` 最后的命令，先 ls 一下：

![image](https://user-images.githubusercontent.com/861659/98482707-863afd00-2246-11eb-9452-64fe7f7cd05a.png)

之后要干什么就很简单了。