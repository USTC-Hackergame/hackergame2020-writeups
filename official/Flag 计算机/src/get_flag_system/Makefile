CC      = gcc
DOS     = dosbox
CFLAGS  = -std=gnu99 -w -O0 -nostdlib -m32 -march=i386 \
  -Wno-unused-function \
  -ffreestanding -fomit-frame-pointer -fwrapv -fno-strict-aliasing \
  -fno-leading-underscore -fno-pic -fno-stack-protector \
  -Wl,--nmagic,-static,-Tcom.ld

dosdef.com : dosdef.c *.h

.PHONY : all clean test

clean :
	$(RM) *.com

test : dosdef.com
	$(DOS) $^

%.com : %.c
	$(CC) -o $@ $(CFLAGS) $<
