#!/bin/sh

unzip ../frames.zip
[ -e repo.tar ] && rm repo.tar
touch repo.tar

for i in frame-*.png; do
echo "$i"
# https://stackoverflow.com/questions/60506222/encode-decode-binary-data-in-a-qr-code-using-qrencode-and-zbarimg-in-bash
# requires zbar >= 0.23.1
zbarimg --raw -q -Sbinary "$i" >> repo.tar
done;

tar -xf repo.tar

rm frame-*