#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

__attribute__((constructor))
void __init(){
    mprotect((void*)0x00401000, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC);
}

int main(){
    void *addr;
    int bit;
start:
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    puts("You can flip only one bit in my memory. Where do you want to flip?");
    scanf("%p %d", &addr, &bit);
    if (bit >= 0 && bit < 8) {
        *(unsigned char*)addr ^= 1 << bit;
        puts("Done.");
        exit(0);
    } else {
        puts("Invalid input");
        goto start;
    }
    return 0;
}
