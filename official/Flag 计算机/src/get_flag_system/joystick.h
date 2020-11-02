#include "math.h"
#include "int.h"

struct joystick {
    uint16_t axis[4];
    bool button[4];
};

struct joystick_config {
    uint16_t min[4];
    uint16_t max[4];
    uint16_t center[4];
};

static struct joystick_config joystick_config = {
    {0xffff, 0xffff, 0xffff, 0xffff},
    {0x0000, 0x0000, 0x0000, 0x0000},
    {0x0000, 0x0000, 0x0000, 0x0000},
};

static void joystick_read(struct joystick *joystick)
{
    asm volatile ("mov  $0x84, %%ah\n"
                  "mov  $1, %%dx\n"
                  "int  $0x15\n"
                  : "=a"(joystick->axis[0]), "=b"(joystick->axis[1]),
                    "=c"(joystick->axis[2]), "=d"(joystick->axis[3]));
    for (int i = 0; i < 4; i++) {
        joystick_config.min[i] =
            min(joystick_config.min[i], joystick->axis[i]);
        joystick_config.max[i] =
            max(joystick_config.max[i], joystick->axis[i]);
    }
    uint16_t buttons = 0;
    asm volatile ("mov  $0x84, %%ah\n"
                  "mov  $0, %%dx\n"
                  "int  $0x15\n"
                  : "=a"(buttons)
                  : /**/
                  : "bx", "cx", "dx");
    for (int i = 0; i < 4; i++)
        joystick->button[i] = !(buttons & (1 << (i + 4)));
}

#include "vga.h"
#include "vga_font.h"

static void joystick_crosshair(struct point c, uint8_t color)
{
    vga_line((struct point){c.x - 2, c.y},
             (struct point){c.x + 2, c.y}, color);
    vga_line((struct point){c.x, c.y - 2},
             (struct point){c.x, c.y + 2}, color);
}

static void joystick_calibrate()
{
    vga_clear(BLUE);
    int32_t scaled[4] = {};
    struct joystick joy;
    do {
        vga_vsync();
        joystick_crosshair((struct point){scaled[0], scaled[1]}, BLUE);
        joystick_crosshair((struct point){scaled[2], scaled[3]}, BLUE);
        joystick_read(&joy);
        for (int i = 0; i < 4; i++) {
            int32_t scale = joystick_config.max[i] - joystick_config.min[i];
            if (scale != 0) {
                scaled[i] = joy.axis[i] - joystick_config.min[i];
                scaled[i] *= (i & 0x01) ? VGA_PHEIGHT : VGA_PWIDTH;
                scaled[i] /= scale;
            }
        }
        joystick_crosshair((struct point){scaled[0], scaled[1]}, WHITE);
        joystick_crosshair((struct point){scaled[2], scaled[3]}, YELLOW);
        vga_print((struct point){55, 80}, YELLOW,
                  "MOVE JOYSTICK AROUND ITS FULL RANGE");
        vga_print((struct point){43, 113}, YELLOW,
                  "THEN CENTER JOYSTICK AND PRESS BUTTON A");
        vga_pixel((struct point){VGA_PWIDTH / 2, VGA_PHEIGHT / 2}, BLACK);
    } while (!joy.button[0]);
    for (int i = 0; i < 4; i++)
        joystick_config.center[i] = joy.axis[i];
    vga_clear(LIGHT_BLUE);
    do
        joystick_read(&joy);
    while (joy.button[0]);
}
