#!/bin/sh

# generate repo.tar
dd if=/dev/urandom of=files/repo/file_1MB bs=1024 count=1000
tar -C files/repo/ -cJf files/repo.tar.xz flag file_1MB
tar -C files/ -cf repo.tar META COMMITS repo.tar.xz

split -b 2953 repo.tar

for i in x*; do
echo "$i"
qrencode -r "$i" -8 -v 40 -o frame-"$i".png;
done;

zip -r frames.zip frame-*.png

# cleanup
rm x*
rm frame-*.png
rm files/repo.tar.xz
rm files/repo/file_1MB