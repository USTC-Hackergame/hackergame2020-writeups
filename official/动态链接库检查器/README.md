# 动态链接库检查器

- 题目分类：binary

- 题目分值：250

`ldd` 是一个方便的 Linux 命令行工具，可以用来检查可执行文件依赖的动态链接库。

考虑到某些尚未安装 Linux 的用户，某同学写了一个在线服务，只要上传 Linux 可执行文件，就可以看到 `ldd` 命令的结果。

注：服务器的环境是 Debian 10，ldd 版本为 ldd (Debian GLIBC 2.28-10) 2.28

**公告：本题中每次上传分析文件的环境是独立的，之前上传的文件不会被保留。**

[打开/下载题目](http://202.38.93.111:10060/?token={token})

---

在 ldd 的 man 手册页中我们可以查到：

```
Security
    Be aware that in some circumstances (e.g., where the program speci‐
    fies an ELF interpreter other than ld-linux.so), some versions of ldd
    may attempt to obtain the dependency information by attempting to di‐
    rectly execute the program, which may lead to the execution of what‐
    ever code is defined in the program's ELF interpreter, and perhaps to
    execution of the program itself.  (In glibc versions before 2.27, the
    upstream ldd implementation did this for example, although most dis‐
    tributions provided a modified version that did not.)

    Thus, you should never employ ldd on an untrusted executable, since
    this may result in the execution of arbitrary code.  A safer alterna‐
    tive when dealing with untrusted executables is:

        $ objdump -p /path/to/program | grep NEEDED

    Note, however, that this alternative shows only the direct dependen‐
    cies of the executable, while ldd shows the entire dependency tree of
    the executable.
```

虽然说 ldd 处理任意的程序是危险的，但常见的 Linux 发行版，包括题目服务器的版本，都避免了这个问题。

在网上搜索「ldd exploit」之类的关键词可以查到 CVE-2019-1010023，在[这个链接](https://sourceware.org/bugzilla/show_bug.cgi?id=22851)中，我们可以看到 ldd 任意命令执行的示例代码，然而这个问题并没有被修复。

所以我们把示例代码保存成文件，把 `shellcode.asm` 最后的 `cat /etc/passwd` 改成读取 flag 的命令 `cat /flag`，然后在 Linux 环境下使用 `make evil` 命令编译，得到的 `libevil.so` 就可以上传到题目的网页获得 flag 了。

[解题代码](src/solution)
