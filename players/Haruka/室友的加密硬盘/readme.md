# 室友的加密硬盘

首先下载下来硬盘之后直接尝试怼到虚拟机里当启动盘启动一下，然后果然掉到了 initrd shell 上。再接着分析太难了，还是挂在一个正常 linux 下玩吧。

现场装了一个 ubuntu 虚拟机，把硬盘挂在上面，看一下分区结构：

![image](https://user-images.githubusercontent.com/861659/98481672-28ef7d80-223f-11eb-8419-7325fe756e18.png)

快速看一眼各个分区的格式：

![image](https://user-images.githubusercontent.com/861659/98481686-4cb2c380-223f-11eb-8107-88092c8d9f50.png)

看来要找的东西在这个 LUKS1 分区里，加密也足够强，看来只能找找从哪能捞出来 key 了。

这个 `sdb7` 看来是尾部截断的，不知道还能捞到多少东西。这种截断的分区是挂载不上的，于是用 hddrescue 把分区 dump 出来，找了个[工具](https://sourceforge.net/projects/ext2read/)尝试读取，结果没捞出来任何有用的信息。

难道 boot 里会有挂载加密分区的 key？挂上一看：

```
# root @ hdd in /mnt/1 [18:59:20]
$ cat keyfile
I'm not that stupid to put plaintext key in /boot!
```

老袁点点点.webp

那唯一剩下的就是这一大块 swap 了，毕竟是内存，兴许里面会有残留在内存里的 key。AES 一般的实现都会在内存里留下所有 schedule 好的 round key，所以有一些工具可以从内存里恢复出来 key（IV 就没戏了）。之前接触过的是 [bulk_extractor](https://github.com/simsong/bulk_extractor)，支持捞 AES key，但我现场找了个更轻量级一点的[工具](https://sourceforge.net/projects/findaes/)。

对着 swap 跑了一下：

![image](https://user-images.githubusercontent.com/861659/98481875-d616c580-2240-11eb-9426-65c9e2439efc.png)

哦豁，东西还不少。根据 file 的结果，分区加密是 aes-xts-plain64，查[资料](https://blog.appsecco.com/breaking-full-disk-encryption-from-a-memory-dump-5a868c4fc81e)得知他的 key 长度是 512 bit，因此应该是跑出来的这些 key 挨着的两个拼在一起。资料显示 key 也是 little endian，因此相邻的两个 key 应该反向拼在一起。

……窝懒，手试太麻烦了，所以快速写了个 python 脚本来拼好所有可能的组合：

（依旧是从 ipython 历史恢复出来的，但应该没问题

```py
keys = """e195501f5bf8fffe5f4c66c43249a5747875c98f9cb598c70f52a0d05f0601bc
d913145b01b203ca068e48d2f40b048639d8c6f4cfe93b22c3795945ca9d9e2a
000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
457895c6ffa897807497bc31320cf9bff6707e176be26a1058fa49a12ccd2762
b895ea5154cea307a3f3891fd43f19c0d54ba38b8dd28519841fa818f24eaefb
082c4400a34b81dbc80de81874cf03ff16d97eb9380c515d3ec48e8433d7dc64
ef3b6d7b80e9ff8b13c8b801984d2c9cf6c0ca8dd342da98112f0c70f34fd5c8
4cdc0c14cb55bb435e75438b7d73f445ed5e90c9514b2d4264c753492bf847e8
9f3330a42a7f6446260df6e2f31d311e2fcfa3d6e1f4736e835b78e63c97ccc3
eab90394d3e9892c87a4b2f32144c71a2b1d2e0cdefce683125d695d6ed81d6c
37d7deb43c0223b8656dd6a862562a1a8360926278dc65f445eda2146844589f
000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
6bc77bd328b378315a193c7dfa0d14c2f023f5565564de40a6ba66d29aedfd3d
31c69dff83847a6c3c3c091e4ff6113ca5799e1b63656f0bd51bd6490c20769c
e4d58f63d629f38803da3c712c5a0cc2be774b9d925d136024a181315d91ac99
136ce9ce0d3f130ebe629570a08bc2ea883e451533875140027d1b3fdb5d0091
31c69dff83847a6c3c3c091e4ff6113ca5799e1b63656f0bd51bd6490c20769c
fa01a98089a38f606c148694e7a3509aaccfc165068ed67f5715384b93e56aa6
e4581675c3f947f7b537a3dd6098e4a5898b0a18c2b3b0f675c61de4106fc6a1
4c82f3493f9a3381f51c394ab8532bd037db64b793057aade3d6bf67cbebf933
fa01a98089a38f606c148694e7a3509aaccfc165068ed67f5715384b93e56aa6
e4581675c3f947f7b537a3dd6098e4a5898b0a18c2b3b0f675c61de4106fc6a1"""
keys = keys.split("\n")
kk = []
for i in range(len(keys)):
    if i > 0:
        kk.append(keys[i] + keys[i-1])
        kk.append(keys[i-1] + keys[i])
print(kk)
```

之后把所有 key 分别写到文件里：

（这个代码都没 ipython 捞着更费劲了

```py
for i, v in kk:
  open("%d.key" % i, "w").write(v)
```

这样一来就得到了所有 hex 格式的可能的 key 文件 `0.key` - `41.key`。在喂给 `cryptsetup` 之前，需要先把这些文件转换成 binary：

```sh
for i in `seq 0 41`; do xxd -r -p $i.key $i.bin; done
```

得到 `0.bin` - `41.bin`。然后就可以尝试分别用这些文件挂载分区了：

```sh
for i in `seq 0 41`; do cryptsetup --master-key-file $i.bin luksOpen /dev/sdb6 t$i; done
```

跑完后输出里有一行

```
Cannot use device /dev/sdb6 which is in use (already mapped or mounted).
```

说明跑出来有重复的 key，那就是已经挂成功了，然后发现多了一个 `/dev/dm-0`，挂上一看：

![image](https://user-images.githubusercontent.com/861659/98482176-ffd0ec00-2242-11eb-9f74-0eb24005b117.png)

打完收工

之后看了一眼挂上的 dm 名字：

```
# root @ hdd in ~ [19:23:31] C:2
$ ls /dev/mapper/
control  t34
```

那说明 `34.key` 里就是真正的 key。