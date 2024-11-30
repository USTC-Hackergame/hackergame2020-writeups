# 室友的加密硬盘

- 题目分类：general

- 题目分值：200

「我的家目录是 512 位 AES 加密的，就算电脑给别人我的秘密也不会泄漏……」你的室友在借你看他装着 Linux 的新电脑时这么说道。你不信，于是偷偷从 U 盘启动，拷出了他硬盘的一部分内容。

压缩包 SHA1: `a8189418c5d534c23943136b51da0a4fcdc354a0`

解压密码：`123rfng19183llli8nlv2`

（附件暂缺）

---

### 先说出题人的预期解

文件根据说明是磁盘镜像，用 fdisk 查看基本情况，就假设文件叫 target 了：

```
$ fdisk -l target.img
Disk target.img: 1.91 GiB, 2048000000 bytes, 4000000 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xa4ee910b

Device      Boot   Start      End  Sectors  Size Id Type
target.img1 *       2048   391167   389120  190M 83 Linux
target.img2       393214 16775167 16381954  7.8G  5 Extended
target.img5       393216  1890303  1497088  731M 82 Linux swap / Solaris
target.img6      1892352  3891199  1998848  976M 83 Linux
target.img7      3893248 16775167 12881920  6.1G 83 Linux
```

确实是磁盘， MBR 分区表，一个主分区，和一些 Linux 扩展分区 。明显文件只有 2GB ，最后一个分区只截取了一点点。

用 dd 提取出单独的分区来：

```
$ dd if=target.img of=boot.img bs=512 count=389120 skip=2048
```

```
$ dd if=target.img of=swap.img bs=512 count=1497088 skip=393216
```

```
$ dd if=target.img of=chome.img bs=512 count=1998848 skip=1892352
```

用 file 查看一下并尝试 mount ，看出主分区是 ext4 格式的 boot 分区； 976M 分区 LUKS 加密，应该是题目中描述的家目录所在分区； swap 内有 SWSUSP1 镜像，表示有休眠存在；最后一个 6.1GB 分区应该只能是根分区了。因为虽然磁盘只得到了一小部分，分区表仍然完整并会显示出所有的分区。

那么之后自然的思路是看看 boot 内有没有东西，毕竟有些不太注意安全的人是会图方便把 LUKS 的key 放在 boot 中以便开机不用输入密码的。于是：

```
$ sudo mount boot.img /mnt
$ cat /mnt/keyfile
I'm not that stupid to put plaintext key in /boot!
```

信不信由你，我是信了。

那怎么办呢？ AES 又不能爆破，那就只有 swap 和根分区有戏了。

根分区只有一点点，但也可以通过 testdisk 之类看看内容，或者 strings 一下... 要是有更多的非预期解那也算是 OK 的。

那就看 swap 吧，既然休眠，那估计整个内存 dump 都在里头了，那就找一下 AES key 吧 -- 这一步萌新出题人不太清楚做题的人能不能想到，出题灵感来源于 cold boot attack ，本想弄一个真实冷启动 dump 出的内存镜像，但鉴于能力和成本不够，就索性用休眠导致的 memory dump 了。

搜索在内存镜像中找 AES key 的方法，我找到了以下几个：

-  [findaes](https://sourceforge.net/projects/findaes/) ，可用；

- [r2](https://github.com/radareorg/radare2) ，可用，似乎更好；
- [aeskeyfind](https://github.com/makomk/aeskeyfind) ，需要指定参数阈值，但也可以得到结果。

以 r2 为例：

```
$ r2 swap_orig.img
 -- I endians swap.
[0x00000000]> /ca
Searching 1 byte in [0x0-0x2db00000]
hits: 12
0x006529d8 hit0_0 d913145b01b203ca068e48d2f40b048639d8c6f4cfe93b22c3795945ca9d9e2a
0x00652b08 hit0_1 000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
0x0737c9d8 hit0_2 37d7deb43c0223b8656dd6a862562a1a8360926278dc65f445eda2146844589f
0x0737cb08 hit0_3 000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
0x0a18ca1a hit0_4 e4d58f63d629f38803da3c712c5a0cc2be774b9d925d136024a181315d91ac99
0x0a18cc0e hit0_5 136ce9ce0d3f130ebe629570a08bc2ea883e451533875140027d1b3fdb5d0091
0x0a32db50 hit0_6 31c69dff83847a6c3c3c091e4ff6113ca5799e1b63656f0bd51bd6490c20769c
0x0b1c873a hit0_7 fa01a98089a38f606c148694e7a3509aaccfc165068ed67f5715384b93e56aa6
0x0b1c890d hit0_8 e4581675c3f947f7b537a3dd6098e4a5898b0a18c2b3b0f675c61de4106fc6a1
0x0bd08b20 hit0_9 4c82f3493f9a3381f51c394ab8532bd037db64b793057aade3d6bf67cbebf933
0x0d013349 hit0_10 fa01a98089a38f606c148694e7a3509aaccfc165068ed67f5715384b93e56aa6
0x0d01351c hit0_11 e4581675c3f947f7b537a3dd6098e4a5898b0a18c2b3b0f675c61de4106fc6a1
[0x00000000]> q
```

嗯，确实有不少的 key 。题目描述密钥是 512 位（这也是 LUKS 分区加密的默认密钥），于是找两个地址相连的 key ，合并起来，尝试作为 LUKS 的 master key 打开分区。注意相连要正反顺序都试一下（应该反向连接）！

这里直接以最终的成功结果为示例了，首先把 key 写入文件：

```
$ echo e4581675c3f947f7b537a3dd6098e4a5898b0a18c2b3b0f675c61de4106fc6a1fa01a98089a38f606c148694e7a3509aaccfc165068ed67f5715384b93e56aa6 | xxd -r -p > key.txt
```

然后尝试用这个 keyfile 给 LUKS 镜像添加一个密码：

```
$ cryptsetup luksAddKey chome.img --master-key-file key.txt
Enter new passphrase for key slot: ( 此处随便输一个密码，比如1 )
Verify passphrase:
```

成功，然后打开分区：

```
$ sudo cryptsetup luksOpen chome.img chome
Enter passphrase for chome.img: ( 此处输入刚才写的密码 )
```

挂载并得到 flag ：

```
$ sudo mount /dev/mapper/chome /mnt
$ cat /mnt/petergu/flag.txt
```

这里不慎透露了出题人信息，抱歉考虑不周。

其实，出题和解题过程完全参考了这两篇文章：

```
https://blog.appsecco.com/breaking-full-disk-encryption-from-a-memory-dump-5a868c4fc81e?gi=f61ce0646b62
```
```
https://access.redhat.com/solutions/1543373
```

注意，第一篇文章中一个有问题的地方是 LUKS 分区的大小和物理分区大小不同（你可以自己创建一个 LUKS 分区实验一下，对于题目，二者差了 4096 字节），所以用里面类似于 `echo "0 <size> crypt aes-xts-plain64 <key> 0 </dev/drive> 4096" | sudo dmsetup create luks-volume` 的方法是不行的，并且具体的加密方式题目中也没有提到。而红帽文章中直接用 master key 添加 key slot 的方法不需要知道这些信息。但本人也不是专业人士，具体细节还要以正规渠道得到的信息为准。

如果你能够搜到这两篇文章，尤其是第一篇（其实还是比较容易搜到的），那应该可以解出这个题了。

本来还想把家目录也只截一半，然后解密之后用 testdisk 把 flag.txt 恢复出来，但好像这样也没有变得更难，就算了。

### 一个非预期解

不知是因为 LUKS 分区打开的时候本该如此，还是出题人操作不慎在分区创建的时候密码复制到了剪贴板上，密码本身明文在 swap 中出现了，所以 strings 一下然后逐个字符串尝试就可以求解。但感觉其实这样做出来也算是正常解法了。密码是什么留作练习。

### 其他可能方法

本题目的制作方法是在虚拟机装装上 xubuntu ，休眠之后 dump 出磁盘的一部分。就算不知道这个过程，一个自然的想法是尝试恢复启动，在 Linux 启动至 initrd 时进行分析（libreliu的思路）。我没有试过，也留作练习。

