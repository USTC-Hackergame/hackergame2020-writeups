#include "port.h"

static void tone_on()
{
    outportb(0x61, inportb(0x61) | 0x03);
}

static void tone_off()
{
    outportb(0x61, inportb(0x61) & ~0x03);
}

static void tone(unsigned frequency)
{
    uint16_t period = 1193180 / frequency;
    outportb(0x42, period & 0xff);
    outportb(0x42, period >> 8);
}
