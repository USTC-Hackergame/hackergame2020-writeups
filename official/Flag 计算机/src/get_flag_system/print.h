static void print(char *string)
{
    asm volatile ("mov   $0x09, %%ah\n"
                  "int   $0x21\n"
                  : /* no output */
                  : "d"(string)
                  : "ah");
}

static void printl(unsigned long n)
{
    volatile char buffer[12];
    int i = sizeof(buffer);
    buffer[--i] = '$';
    if (n == 0)
        buffer[--i] = '0';
    else
        for (; n > 0; n /= 10)
            buffer[--i] = '0' + (n % 10);
    print((char *) buffer + i);
}
