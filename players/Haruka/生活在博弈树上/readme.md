# 生活在博弈树上

下载下来代码后发现是个普通的井字棋程序，但电脑先手，所以因为游戏的性质我是完全赢不了的（只要算法没问题的话）。加上题目类别是 binary，于是从安全角度分析一下代码，很快发现：

```c
    bool success = false;  // human wins?
    char input[128] = {};  // input is large and it will be ok.
    ...
    printf("Your turn. Input like (x,y), such as (0,1): ");
    gets(input);
```

哦豁，看来直接溢出一下就能抹掉 `success` 了。因为是 64 位程序，所以看上去直接构造一个 136 个字节的 payload 然后让他最后 8 个字节是 `\x01\x00\x00\x00\x00\x00\x00\x00` 就可以了。

……然后因为我太蠢根本没注意看程序实际上栈的位置：

![image](https://user-images.githubusercontent.com/861659/98471999-47e81280-2233-11eb-9a5f-44f96eb8cd51.png)

所以实际上应该是需要 144 字节的 payload 然后让最后一个字节是 `\x01` 即可。

…………但我当时根本就没有发现，结果试了半天都没成功拿到结果。所以我换了个思路，直接把程序返回地址（图中 `r`）写成成功后要执行代码的位置（`0x402551`, `lea     rdi, ...`），构造了一个新的 payload （`r` 位置对应内容是 `\x51\x25\x40\x00\x00\x00\x00\x00`）提交，最终也可以得到 flag。

（我做完第二问都没发现我为什么没能抹掉 `success`，果然我太蠢

<hr>

第二问显然需要拿到 shell（并且第一问的 flag 也提示了），那么最先想到的是直接在栈上那一大段 `input` 里写个 shellcode 然后把返回地址打过去就行了。

……然后本地测试发现，它吐核了。*(core dumped)*

检查文件发现：

```
# mrx @ raw in ~ [2:39:17]
$ checksec/checksec.sh --file tictactoe
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Partial RELRO   Canary found      NX enabled    Not an ELF file   No RPATH   No RUNPATH   tictactoe
```

文件启用了 NX，因此栈上写进去的 shellcode 是不能执行的。（看上去 canary 应该是误报，要不然我第一问的奇葩做法就应该失败了）

因此考虑用 ROP 来搞他一波，于是用 ROPgadget：

```
# mrx @ raw in ~/ROPgadget on git:master o [2:43:21]
$ ./ROPgadget.py --binary ../tictactoe --ropchain  --dump
...
```

ROPgadget 最后会输出一大段 python 代码，根据上图栈结构，在代码开始的 padding 位置需要有 152 字节的内容，因此在生成的代码顶上的 `p = ''` 位置填上 152 字节的垃圾即可。略微改一下代码让他把最后的 `p` 输出出来就能拿到我们需要的 payload。

直接把这个 payload 打过去，正常运行完程序就能拿到 shell 了，ls 就能发现 flag 文件，cat 就完事了。

（然后才反应过来，静态编译进去整个 c library 原来是为了提供 gadget 用的，要不然这点程序肯定没办法构造出来一个完整的 rop chain

（吐核是很早很早之前的实际翻译，但实在太逗了，所以我还是很喜欢用这个翻译

<hr>

附：我打二进制 payload 的方法

直接在终端里没办法往 nc 打二进制，但我又不想用 python 处理这些玩意。于是我用了 fifo 来往 nc 里打任意内容。

（方法来自[这里](https://superuser.com/questions/1307732/how-to-send-binary-data-in-netcat-to-an-already-established-connection/1307773)）

首先创建一个 fifo 文件：

```sh
mkfifo a
```

之后保持 fifo 打开状态：

```sh
exec 3> a
```

3 是为了避开 `stdin stdout stderr` 以免往 fifo 文件里打进去不必要的内容。

之后运行 nc 的时候就可以用 fifo 文件作为输入：

```sh
nc -v <server> <port> < a
```

之后只需要任意往 fifo 文件中写要发送的内容即可。