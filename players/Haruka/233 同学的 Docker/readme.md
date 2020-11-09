# 233 同学的 Docker

首先先打开提供的 [docker hub 链接](https://hub.docker.com/layers/8b8d3c8324c7/stringtool)，看看镜像的命令列表：

![image](https://user-images.githubusercontent.com/861659/98470501-58938b00-2229-11eb-8ad0-b18bcbf6928d.png)

看来在 27 行产生的 layer 里是有这个 flag.txt 的，但是 docker 并不能把单独的 layer 变成 image 来直接运行。不过既然他是单独的 layer，那么在 `/var/lib/docker/overlay2` 里就会有单独的存储。于是找一台机器 pull 下来 image 然后直接：

```
# root @ raw in /var/lib/docker/overlay2 [1:19:43] C:1
$ find . -name flag.txt
./a157ba22c673b129100e1ce354675310999907a6aa3d401182d6096a2f78c76d/diff/code/flag.txt
./fbb84b65568eda68e1fe72399e28de06eace16524cc8603cf8b96b6a0c84a0ab/diff/code/flag.txt
```

于是打开文件就能看到 flag 内容了。

（顺便这个 flag 的内容好尬啊……