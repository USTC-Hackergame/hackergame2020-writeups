#include "int.h"
#include "vga.h"

/* Letters are 7 pixels tall and 5 pixels wide. */

/* http://redd.it/2ba3g3 */
static const char LINES[]   = "BCDEIKOPQRSTUVYZ\\_`";
static const char LETTERS[] =
    "DFJSJJJRJJRJJRGJIIIJGRJJJJJRSIIRIISSIIRIIIHIILJJHJJJSJJJGDDDD"
    "DGAAAAAJHJKMOMKJIIIIIISJQNJJJJJJPNLJJGJJJJJGRJJRIIIGJJJNGCRJJ"
    "RMKJGJIGAJGSDDDDDDJJJJJJGJJJJJFDJJJNQJJJJFDFJJJJFDDDDSABDEIS";

static int vga_font_line(int c, int row) {
    return c == ' ' ? 0 : LINES[LETTERS[(c - 'A') * 7 + row] - 'A'] - 'A';
}

static void vga_print(struct point p, uint8_t color, const char *message)
{
    for (int y = 0; y < 7; y++) {
        for (int x = 0; message[x]; x++) {
            int c = message[x];
            int line = vga_font_line(c, y);
            for (int i = 0; i < 5; i++) {
                if ((line >> i) & 0x01) {
                    int dx = p.x + x * 6 + (4 - i);
                    int dy = p.y + y;
                    vga_pixel((struct point){dx, dy}, color);
                }
            }
        }
    }
}
