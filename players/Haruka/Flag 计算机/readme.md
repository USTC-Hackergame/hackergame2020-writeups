# Flag 计算机

我对这道题真的是又爱又恨：爱的是他出的角度，恨的是他的 bug 真的是多……

这应该是我玩的最开心的一道题，但也因为 bug 浪费了过多时间（我的一血啊啊啊啊

<hr>

拿到 exe，先直接跑一下看看：

![image](https://user-images.githubusercontent.com/861659/98498715-d20f9580-228a-11eb-83f7-71eb84cea911.png)

有点个性，那只能拉到 IDA 里看看了：

![image](https://user-images.githubusercontent.com/861659/98499427-d76ddf80-228c-11eb-8a48-0f850035aff3.png)

wut?

一个一个函数里面都翻了一遍，甚至也没找到任何可疑的东西，看起来都是普通的库函数。

直接拖到 010 里面看看，兴许在某些 header 上藏了东西？

![image](https://user-images.githubusercontent.com/861659/98499841-1ea8a000-228e-11eb-985a-73f14409b526.png)

看上去各种 header 也正常……然后发现 hex 里面并没有常见的 `This program cannot be run in DOS mode` 字样，取而代之的是一大坨不知道是啥的东西，而这一段就是 dos code。

我：这太邪门了

合着这个程序是个 dos 程序然后打进去了一个瘟逗死的部分，主要逻辑都在 dos 程序里面。重新拖一下 IDA，打开文件的时候选上我觉得有生之年不会用到的选项：

![image](https://user-images.githubusercontent.com/861659/98500311-857a8900-228f-11eb-884f-ec87b29ad7c6.png)

加载之后：

![image](https://user-images.githubusercontent.com/861659/98500407-beb2f900-228f-11eb-871a-d942c0b3b9a3.png)

看上去主要逻辑确实是在这个里面没错了。然而 16-bit 程序的问题在于大概轰不了 F5：

![image](https://user-images.githubusercontent.com/861659/98500798-beffc400-2290-11eb-9dc9-d398d4cd8b1a.png)

哦，用错 IDA 了，拖到 32 位班里重新轰一下：

![image](https://user-images.githubusercontent.com/861659/98500852-e9ea1800-2290-11eb-88fc-4ee460d8fd6b.png)

果然 16 位程序没法反编译。既然 ida 不行，那看看 retdec 能不能吃：

![image](https://user-images.githubusercontent.com/861659/98500922-16059900-2291-11eb-8a05-3a32be4cadb8.png)

retdec 直接认成了 64 位文件，看来需要改一下 exe 的 header 让他变成老式程序。这一步只需要干掉 `0x3C` 位置的 `AddressOfNewExeHeader` 即可，保存成新文件再试试：

![image](https://user-images.githubusercontent.com/861659/98501086-8d3b2d00-2291-11eb-85bb-a904e07a731c.png)

看来 retdec 也处理不了 16 位程序，那只能上 ghidra 试试看了：

![image](https://user-images.githubusercontent.com/861659/98501206-ddb28a80-2291-11eb-8b31-8d69478d0b42.png)

某种意义上他还真的能“反编译”出来，但扫了一眼生成的代码内容……

我：这 tm 还不如直接看汇编方便

于是下一步看来只能是对着汇编人工反编译了。不过看上去既然都是最高 386 的指令集，人工反编译应该也不会遇到太多麻烦。

（后来我搜了一下似乎是有专门反编译 16 位 dos 程序的反编译工具的，但我也没有再尝试，有兴趣的可以自己下下来跑一跑，可能会比人工反编译效率高？

我在反编译的时候选择了“总之全都反编译一下”的策略，因此上来就在 VGA 处理和画图上用了相当多时间，不过也人工还原出来了相当多无关逻辑，比如开头的：

![image](https://user-images.githubusercontent.com/861659/98501864-c7a5c980-2293-11eb-9d9d-4b248132043a.png)

将显示模式切换到 VGA 模式（著名的 mode 13h），以及将 `es` 设置为 `A000h` （VGA 的显示内存段地址）；以及

![image](https://user-images.githubusercontent.com/861659/98501999-36832280-2294-11eb-8abc-8ee49579af6a.png)

用指定颜色清空屏幕内容，对应的 C 代码其实整理后大约就是：

```c
void remove_screen_with_color(int color) {
	memset(vga_mem, color & 0xff, 64000); // 320x200
}
```

以及各种打印内容的函数，事实上看上去整个程序大部分代码都消耗在屏幕内容的输出上（

<hr>

（进入严肃模式

这里要注意一点的是 DOS 程序分两种，分别是 .COM 和 .EXE 格式，两种格式加载到内存中时使用的方式并不一样。这道题的程序是 .EXE 格式，而 EXE 文件加载时本题相关部分如下：

1. ES 和 DS 地址设置为 PSP 地址
2. SS 地址设置为程序起始地址 + 文件头中 InitialRelativeSS
3. CS 地址设置为程序起始地址 + 文件头中 InitialRelativeCS

其中 PSP 为 [Program Segment Prefix](https://en.wikipedia.org/wiki/Program_Segment_Prefix)，是 DOS 系统储存程序状态的结构。DOS 在加载程序时会选择最低的空闲地址加载 PSP 并设置上 ES 和 DS。程序起始地址通常会在紧接着 PSP 的位置上，DOS 会将程序加载到起始地址上。而 PSP 长度为 `100h`，因此起始地址在段地址上通常是 `DS + 10h`。本题的程序中，文件头里两个段地址的偏移均为 0， 因此程序加载完成后实际段地址应为 `SS = CS = DS + 10h = ES + 10h`。本题代码中，除 `ES` 在设置视频模式时设置为了 `A000h` 即 VGA 内存地址之外，其他段寄存器均没有变化。

[参考资料](http://www.techhelpmanual.com/829-program_startup___exit.html)

另外需要注意的是，X86 处理器在使用基地址 + 偏移量或间接寻址的寻址模式时，如果参数中包含 `BP` 或者 `SP`，则默认段地址使用 `SS`（栈操作），否则使用 `DS`。（取代码指令永远使用 `CS`。）

用本题程序中一段代码为例：

![image](https://user-images.githubusercontent.com/861659/98508181-65a09080-22a2-11eb-971b-1f08eee32b0f.png)

这里将数字 `2E3Ch` 压栈，作为函数参数传给函数 `_strlen`（本题中的一个获取给定字符串长度的函数）。`_strlen` 函数代码如下：

![image](https://user-images.githubusercontent.com/861659/98508379-bca66580-22a2-11eb-9a4b-8de1c21b4205.png)

`str` 为栈上传入的参数。注意在 `CS:0F55` 位置上的指令 `mov eax, [esp+10h+str]` （或写作 `mov eax, [esp+14h]`） 中，实际执行的指令为 `mov eax, ss:[esp+10h+str]`，所取到的值为栈上参数的值，这里是调用函数时压进去的 `2E3Ch`。接下来 `v1` 初始值为 0，因此第一次在 `CS:0F5E` 位置上的指令 `mov al, [eax]` 实际上是 `mov al, ds:[2E3Ch]`。注意在本题程序中，`CS = DS + 10h`，因此同样的内存位置在 `CS` 上对应的地址应该是 `CS:2D3C`。

如果在 IDA 中直接将 `2E3Ch` 变为字符串引用，IDA 会误认为引用的地址是 `CS:2E3C`，所跳转或显示的字符串将会不正确。（本题程序中通常为显示成从某个字符串中间开始，或者引用到字符串之后的其他数据中。

（在第一版程序中，这个问题也导致了一个不太影响输出结果的 bug。之后会再提到。

<hr>

虽然还原无关逻辑确实浪费了一些时间（我甚至还认真还原了一下），但在过程中发现了 `CS:1632` 处调用的函数（这里我已经改名成了 `init_time`：

![image](https://user-images.githubusercontent.com/861659/98511010-7273b300-22a7-11eb-9eaf-7d03e5be1138.png)

![image](https://user-images.githubusercontent.com/861659/98511035-7e5f7500-22a7-11eb-8aef-9dc5f18aa02a.png)

对应的大概的 C 代码：

```c
typedef struct {
	union {
		struct {
			uint8_t hour;
			uint8_t minute;
			uint8_t second;
			uint8_t ss;
		};
		uint32_t value;
	};
} Time;

Time get_current_time() {
	return *(Time *)dos_get_current_time(); // fake signature!
}

void init_time() {
	Time time = get_current_time();
	*(uint32_t *)0x345c = time.value % 58379;
	*(uint32_t *)0x3404 = 0x41c64e6d;
}
```

这里使用 DOS 系统调用获取了系统时间，并将其数据 `% 58379` 后写入地址 `345Ch`，并初始化了 `3404h` 处变量的内容。联想到题目描述中，

> 但如果在**合适的时间**运行它的话，它就可以告诉你真正的 flag。

这里大概就是需要时间输入的地方了，那么 `345Ch` 和 `3404h` 处的变量大约就是和 flag 相关的关键内容。

回到主函数继续往下看，紧接着是一个 15 次的循环，其中在 `CS:1647` 处调用了 `CS:1012` 的函数，看上去是在将上面初始化的两个变量进行打乱：

```c
int sub_1012() {
	*(uint32_t *)0x3404 = *(uint32_t *)0x3404 * *(uint32_t *)0x345c + 12345678;
	return *(uint32_t *)0x3404;
} 
```

并且每次执行后将 `3404h` 处的变量返回，在主函数中将内容存在 `esp + 68h` 的局部变量中（这里姑且叫做 `result`）。那么 `result` 大概类型就是个 `uint32_t[15]`，估计后面会参与 flag 计算。

之后的代码是一个两层循环嵌套，其中虽然有大量打印屏幕内容的代码，但每次循环开始时（`CS:1694 - CS:1726`）处有很可疑的代码，并用到了局部变量 `result`。整理后发现逻辑如下：

```c
	for (int v2 = 0; v2 <= 14; v2 ++) {
		for (int v3 = 0; v3 <= 14; v3 ++) {
			((uint32_t *)0x3420)[v2] = (
				((uint32_t *)0x3420)[v2] + (
					result[v3] * ((uint32_t *)0x2920)[v3 + v2 * 15]
				) & 0xffff
			) & 0xffff;
			remove_screen_with_color(0x11);
			// paint progress
			for (int v4 = 0; v4 < 0xff; v4 ++) {
				// waste time
			}
		}
	}
```

看来又算了好多东西然后存在了 `3420h` 处的变量里，类型看起来也是个 `uint32_t[15]`，而 `2920h` 处的变量看上去是个 `uint32_t[15][15]` 的提供初始值的变量。大概下面 `3420h` 处的变量会用来算 flag 吧……这条线拉的好长啊！

这整个循环除了计算了 `3420h` 变量的值之外，主要工作是浪费一下程序执行的时间，因为其中有很多 `sleep` 调用，以及反复往屏幕上打印东西本身也比较慢。在这里可以通过修改一部分循环参数以及函数调用参数来尽可能缩短一轮执行的时间，便于后面调试程序。

最终整个循环结束后，程序将视频模式恢复为标准的 80x25 文本模式，并打印最终提示文字，之后在 `CS:1B12 - CS:1B2D` 处的代码将 `32C0h` 处的变量复制到……VGA 内存上？？（`rep movsd` 指令执行内容为将 `DS:SI` 的内容复制到 `ES:DI` 上，共 `CX` 次

代码中本来读出了局部变量 `esp+4h` （这里叫做 `var_148`）的地址，并看上去本来是想将 `32C0h` 变量的内容复制进去，但不知什么原因却复制到了 VGA 内存上。先不管，假设他确实复制到局部变量里面了。

接下来 `CS:1B30 - CS:1B9F` 处的 30 次循环再次用到了 `3420h` 处的变量和局部变量 `var_148`，（但同学这个局部变量看上去并没有正常初始化耶……），将内容一番计算后写入 `esp+40h` 处的局部变量，类型为 `char`，那么这个变量猜测正确定义大概就是 `char flag[30]` 了。果然循环结束之后将这个变量的地址取出来，然后……直接扔给了 DOS 系统调用的打印字符串？

![image](https://user-images.githubusercontent.com/861659/98514395-ba490900-22ac-11eb-83f5-e6fa17095964.png)

问题在于这里取出来的内存地址是 `ss:[esp+14Ch+flag]`，而打印时寻址使用的是 `DS` 段，这里又发生了 `100h` 长度的偏移。不过还好这里最终导致了打印的内存地址比预期地址更小，最终会导致先打印出来 256 字节的垃圾，然后才会打印出来 `flag` 变量的内容。（这里注意，DOS 系统调用的打印字符串是 `$` 结尾的字符串，如果前 256 字节正好遇到了 `$` 字符则会导致打印不到实际 `flag` 变量内容。）

到此整个程序的逻辑已经整理清楚了（除了两处看上去非常像 bug 的地方），我也对着汇编写出来了一份[编译不了的 C 代码](get_flag_system_1.c)，便于照着实现。

接下来就是整理一下各个使用过的变量的初始值，以及将整个逻辑用 python 实现一下，因为时间输入时有一个 `% 58379` 的操作，我们的代码中只需要遍历一下这个空间即可得到 flag。

……然而跑完了一圈，最终也没能筛选到 flag 内容。

考虑到程序里有一个栈内容没能正常初始化的地方，我是不是应该假设没初始化的内容全都是 `0x0`？

……然而又跑了一圈，还是没有结果。

我编译了一份 dosbox-x 的 debug 版，把程序塞进去下断点调试，最后发现我的代码中内存最终状态的值和 dosbox 中程序的输出是一致的。

……难道 dosbox 准确性不太行？

我拿出了之前装过 DOS 的 PCem 虚拟机，把程序塞进去用 `debug`  下断点调试，发现我算出来的内容不一样了。仔细观察内存内容后发现，未初始化的栈上内容并不是 0，而是预期中的不知道是什么垃圾。抱着死马当活马医的心态，我把栈上的垃圾手敲了出来，又跑了一遍算法，确保我的算法最终状态和 PCem 里程序的最终状态一致，然后再遍历一次。

……依旧什么都没有。

到这里我已经非常确信程序本身存在了问题并进行了反馈，果然不久后程序就临时下架了（（

<hr>

one\_eternity\_later.mp4

第二天程序重新上架后，迅速观察了一下，发现主要有三点变化：

首先，最显眼的地方是

![image](https://user-images.githubusercontent.com/861659/98516156-79062880-22af-11eb-8e61-32b2461f36ae.png)

在往栈上复制 `32C0h` 处变量内容时，程序提前将 `ES` 设置成了 `SS`，这样复制就会正确执行了。

其次，往下一看最终打印 flag 时的代码：

![image](https://user-images.githubusercontent.com/861659/98516356-c08cb480-22af-11eb-8f10-ff180167dc6c.png)

这里读出了无关变量的地址，检查栈结构发现这里已经正确(?)处理了段地址不一致导致的偏移。

之后检查了一下所有变量的初始值，发现 `3420h` 处变量的初始值也发生了变化：

老版本：

![image](https://user-images.githubusercontent.com/861659/98516654-1b261080-22b0-11eb-8a74-3499aa41c158.png)

新版本：

![image](https://user-images.githubusercontent.com/861659/98516703-2c6f1d00-22b0-11eb-9a1b-99174c19c982.png)

从不知道什么初始数据全部变成了初始为 0。

二话不说直接改一下 python 实现的代码，重新跑一圈。

……然后打印出来了一万个一样的 flag。立刻提交成功，拿到一血。

最后数了一下，一共有 228 种初始状态可以实际跑出最终的 flag，因此如果什么都不做只反复运行程序的话，也有大约 0.39% 的概率跑出来最终 flag。不过考虑到程序中有大量故意浪费时间的代码，如果不对相关地点进行 patch，那么平均每跑一次需要消耗 1 分钟左右，需要一定的毅力才能暴力跑出来结果。（不过如果已经读懂代码到能 patch 相关地点了，那么相信复制算法也不应该是难事了

最终的 python 实现代码在[这里](dosflag.py)。（可以从程序的一些注释里感受一下我是如何被 bug 折磨的
