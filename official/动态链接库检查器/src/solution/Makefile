all:
	gcc -fPIC -shared evil.c -o libevil.so
	gcc main.c -levil -L. -o main -Wl,-rpath,./
	gcc make_evil.c -o make_evil -g
evil: all
	nasm -fbin shellcode.asm -o shellcode.bin
	gcc -fPIC -shared evil.c -T evil.script -o libevil.so
	./make_evil
clean:
	rm main libevil.so

gdb:
	gdb /home/blackzert/kernel_experiments/glibc_build/elf/ld.so

list:
	/lib64/ld-linux-x86-64.so.2 --list ./libevil.so
