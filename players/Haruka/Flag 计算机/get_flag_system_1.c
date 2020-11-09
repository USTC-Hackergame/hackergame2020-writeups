#include <stdlib.h>
#include <string.h>

int VGA_256 = 0x13;
int TEXT_80_25 = 0x3;

uint8_t vga_mem[200][320];

// ds = cs - 0010
// naked literal pointers are ds

typedef struct {
    short x;
    short y;
} Coord;

typedef struct {
    union {
        struct {
            uint8_t hour;
            uint8_t minute;
            uint8_t second;
            uint8_t ss;
        };
        uint32_t value;
    };
} Time;

void set_video_mode_vga() {
    set_video_mode(VGA_256);
}

void set_video_mode_text() {
    set_video_mode(TEXT_80_25);
}

void remove_screen_with_color(int color) {
    memset(vga_mem, color & 0xff, 64000); // 320x200
}

void wait_vsync() {
    uint8_t status;
    do {
        status = get_vga_status();
    } while (status & 8); // vsync pulse
    do {
        status = get_vga_status();
    } while (!(status & 8));
}

short _strlen(char *a1) {
    return strlen(a1);
}

short get_centered_x_coord(int len) {
/*  eax = 0x35 - a1 & 0xffff;
    edx = (unsigned int)eax >> 31;
    eax += edx;
    eax >>= 1;
    edx = eax;
    eax <<= 1;
    eax += edx;
    eax <<= 1;
    return eax; */
    return 6 * ((uint16_t)(0x35 - len) / 2);
}

int sub_057c(uint8_t ch, int a2) {
    if (ch == ' ') {
        return 0;
    }
    int tmp = a2 + ch * 7 - 0x1c7;
    int res = *((char *)0x2d00 + tmp) - 'A';
    res = *((char *)0x2ce0 + tmp) - 'A';
    return res;
}

void paint_coord(Coord coord, uint8_t color) {
    if (coord.x < 0 || coord.x >= 320) {
        return;
    }
    if (coord.y < 0 || coord.y >= 200) {
        return;
    }
    vga_mem[coord.y][coord.x] = color;
}

void paint_line(Coord anchor, uint8_t color, char *data) {
    int i, col, ch, v5, x, y;
    Coord coord;
    for (int line = 0; line <= 6; line ++) {
        for (i = 0; data[i]; i ++) {
            char ch = data[i];
            v5 = sub_057c(ch, line);
            for (col = 0; col <= 4; col ++) {
                if (!((v5 >> (col & 0xff)) & 1)) {
                    continue;
                }
                x = i * 6 + anchor.x - col + 4;
                y = line + anchor.y;
                coord.x = x;
                coord.y = y;
                paint_coord(coord, color);
            }
        }
    }
}

void sleep(int time) {
    system_wait(time >> 16, time & 0x16);
}

void _wait() {
    for (short v1 = 0; v1 <= 14; v1 ++) {
        sleep(800);
    }

}

Time get_current_time() {
    return *(Time *)dos_get_current_time(); // fake signature!
}

void init_time() {
    Time time = get_current_time();
    *(uint32_t *)0x345c = time.value % 58379;
    *(uint32_t *)0x3404 = 0x41c64e6d;
}

int sub_1012() {
    *(uint32_t *)0x3404 = *(uint32_t *)0x3404 * *(uint32_t *)0x345c + 12345678;
    return *(uint32_t *)0x3404;
} 

int main() {
    set_video_mode_vga();
    remove_screen_with_color(0x11); // 01 gray
    wait_vsync();
    short len = _strlen((char *)0x2e04);
    short res2 = get_centered_x_coord((int)len);
    Coord coord = { .x = res2, .y = 0xe };
    paint_line(coord, 5, (char *)0x2e04);
    // painting first circle
    _wait();
    remove_screen_with_color(0x11);
    init_time();
    uint32_t result[15] = { 0 };
    for (int v1 = 0; v1 <= 14; v1 ++) {
        result[v1] = sub_1012();
    }
    for (int v2 = 0; v2 <= 14; v2 ++) {
        for (int v3 = 0; v3 <= 14; v3 ++) {
            ((uint32_t *)0x3420)[v2] = (
                ((uint32_t *)0x3420)[v2] + (
                    result[v3] * ((uint32_t *)0x2920)[v3 + v2 * 15]
                ) & 0xffff
            ) & 0xffff;
            remove_screen_with_color(0x11);
            // paint progress
            for (int v4 = 0; v4 < 0xff; v4 ++) {
                // waste time
            }
        }
    }
    remove_screen_with_color(0x11);
    // paint progress again
    for (int v5 = 0; v5 < 0xff; v5 ++) {
        for (int v6 = 0; v6 < 160; v6 ++) {
            // really empty
        }
    }
    _wait();
    set_video_mode_text();
    dos_print_string(); // ending messages

    short v148[30];
    memcpy(&v148, 0x33c0, 30 * 2);
    
    char flag[30];
    for (short v7 = 0; v7 < 30; v7++) {
        flag[v7] = (((uint32_t *)0x3420)[v7 % 15] ^ v148[v7]) & 0xff;
    }
    dos_print_string(flag);

}