#ifndef TIME_H
#define TIME_H

static uint32_t get_tick()
{
    unsigned long result;
    asm volatile ("push  %%es\n"
                  "mov   $0,%%bx\n"
                  "mov   %%bx,%%es\n"
                  "mov   $0x046C,%%bx\n"
                  "mov   %%es:(%%bx),%%eax\n"
                  "pop   %%es\n"
                  : "=a"(result)
                  : /* no inputs */
                  : "bx");
    return result;
}

static uint32_t get_time()
{
    uint16_t high, low;
    asm volatile ("mov  $0x2C, %%ah\n"
                  "int  $0x21\n"
                  : "=c"(high), "=d"(low)
                  :
                  : "ah");
    return (((uint32_t) high) << 16) | low;
}

/* Granularity of 976 usec and doesn't work in DOSBox. */
static void usleep(uint32_t us)
{
    asm volatile ("mov   $0x86, %%ah\n"
                  "int   $0x15\n"
                  : /* no outputs */
                  : "c"(us >> 16), "d"(us & 0x16)
                  : "ah", "flags");
}

/* Granularity of 55 msec. */
static void msleep(int ms)
{
    uint32_t count = ms / 54; // 18.2 Hz
    uint32_t last = get_tick();
    while (count) {
        uint32_t now = get_tick();
        if (now != last) {
            last = now;
            count--;
        }
    }
}

#endif
