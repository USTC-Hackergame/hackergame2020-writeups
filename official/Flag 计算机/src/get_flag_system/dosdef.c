#include "init.h"
#include "print.h"
#include "joystick.h"
#include "vga.h"
#include "rand.h"
#include "time.h"
#include "alloc.h"
#include "keyboard.h"
#include "speaker.h"

#define SCALE              1000
#define BACKGROUND         17
#define PLAYER             14
#define BULLET_SPEED       3
#define PARTICLE_MAX_AGE   50
#define MAX_PLAYERS        2

typedef unsigned int tick_t;
typedef void (*ai_t)(int id);
typedef void (*power_t)(int id);

static tick_t ticks;
static unsigned score;
static unsigned best_score;
static struct speaker speaker;

struct ship {
    int32_t x, y, dx, dy;
    tick_t last_fire;
    ai_t ai;
    struct sample *fx_fire;
    uint16_t score;
    uint16_t hp, hp_max;
    uint8_t radius;
    uint8_t fire_delay;
    uint8_t fire_damage;
    uint8_t drop_rate;
    uint8_t color_a, color_b;
    bool is_player;
    union {
        int target_ship;
        struct {
            uint32_t x, y;
        } target_position;
    };
};

struct bullet {
    int32_t x, y, dx, dy;
    tick_t birthtick;
    uint8_t color;
    uint8_t damage;
    bool alive;
};

struct particle {
    int32_t x, y;
    tick_t birthtick;
    bool alive;
};

struct powerup {
    int32_t x, y;
    tick_t birthtick;
    power_t power;
    bool alive;
    uint8_t color;
};

static struct bullet *bullets;
static size_t bullets_max = 32;

static struct particle *particles;
static size_t particles_max = 64;

static struct ship *ships;
static size_t ships_max = 12;

static struct powerup *powerups;
static size_t powerups_max = 8;

static bool joystick_detected()
{
    struct joystick joystick;
    joystick_read(&joystick);
    return joystick.axis[0] != 0 || joystick.axis[1] != 0;
}

static void burn(int32_t x, int32_t y);
static void ship_draw(int id, bool clear);
static void powerup_random(int id);


// #define VGA_PWIDTH  320
// #define VGA_PHEIGHT 200
// 53 character a line

static unsigned short strlen(const char * in)
{
    short ret=0;
    while(in[ret] != 0)
    {
        ret++;
    }
    return ret;
}

static unsigned short str_line_middle(unsigned short length)
{
    return (53 - length) / 2 * 6;
}

static void delay()
{
    for(unsigned short i = 0; i<0xf;i++)
    {
        usleep(800);
    }
}


// static uint32_t rand_seed = 375226057;

// static uint32_t rand(void)
// {
//     rand_seed = rand_seed * 1103515245 + 12345;
//     return rand_seed;
// }

// static uint32_t randn(uint32_t n)
// {
//     return (rand() >> 7) % n;
// }




uint32_t a,x0,b;

static uint32_t gen_random_a()
{
    a = get_time() % 58379;
    // a = 26141;
    x0 = 1103515245;
}

static uint32_t myrand(void)
{
    x0 = x0 * a + 12345678;
    return x0;
}

// flag{g3tfl4g_0p3r4t1ng_syst3m}
uint32_t get_matrix[15];
uint32_t my_matrix[15*15]={20597,19141,29258,17804,29076,28746,24890,28979,26196,31833,26624,24774,18916,29028,24033,22913,23436,25750,26539,21652,31296,22446,16506,21949,22761,30221,29477,29617,16497,23022,23179,30781,23877,29171,31665,26534,32159,22583,27525,28708,31216,17158,31988,32190,23747,21272,21278,24727,29984,25303,23445,23119,23155,26346,26389,30747,28948,31418,21323,31758,30911,18790,21312,25099,22348,25409,29357,22180,23588,28794,18133,25624,21972,23401,24821,31369,25187,31517,19840,28836,20794,20239,24523,30814,24016,17954,21227,16691,30290,23391,20482,24822,31968,30651,27908,22690,30875,31003,31747,19978,25482,18563,30143,27788,26658,26295,23244,27086,26456,24251,28647,22783,27460,19187,23252,24078,19203,26251,18113,19542,24533,16666,24038,32744,28670,30438,26379,18591,30109,26509,20947,27696,22945,27542,32128,25416,21675,19389,27085,29380,20163,21102,30936,30862,18230,21904,16938,16579,20641,27551,22740,24666,16836,23306,27661,26506,28623,29816,20166,29405,23982,30046,19365,24926,19029,32448,17567,17156,18678,28594,19769,28631,25769,31309,24457,30625,21825,29811,17112,31370,25345,24333,24005,31606,30942,21441,30599,22894,18015,19994,27901,26868,21948,27614,23449,21289,19588,19955,28133,16696,31509,26219,19946,27895,28760,28547,28315,16614,26006,17129,24769,24608,17714,17682,18532,17597,29247,28789,27011,29841,32640,17508,27662,23548,29514};


int dosmain(void)
{

    vga_on();
    vga_clear(BACKGROUND);
    vga_vsync();
    
    vga_print((struct point){str_line_middle(strlen("WWWWWWWWWWWWWOOOOOOOOOOWWWWWOO OOOOOOOWWWWWWWWWWWWWWW")), 14},  MAGENTA, "WWWWWWWWWWWWWOOOOOOOOOOWWWWWOO OOOOOOOWWWWWWWWWWWWWWW");
    vga_print((struct point){str_line_middle(strlen("WWWWWWWWOOO         OONWWWWWOOO         OOOWWWWWWWWWW")), 23},  MAGENTA, "WWWWWWWWOOO         OONWWWWWOOO         OOOWWWWWWWWWW");
    vga_print((struct point){str_line_middle(strlen("WWWWWWOOO       OOOdOOWWWWMMWOOdOOO       OdOWWWWWWWW")), 32},  MAGENTA, "WWWWWWOOO       OOOdOOWWWWMMWOOdOOO       OdOWWWWWWWW");
    vga_print((struct point){str_line_middle(strlen("WWWWWOO      OOdONWOOOdOOOOOdOOOWNOOO       OOWWWWWWW")), 41},  MAGENTA, "WWWWWOO      OOdONWOOOdOOOOOdOOOWNOOO       OOWWWWWWW");
    vga_print((struct point){str_line_middle(strlen("WWWNOO      OONWOOOOO         OOOOOWOOO      OOWWWWWW")), 50},  MAGENTA, "WWWNOO      OONWOOOOO         OOOOOWOOO      OOWWWWWW");
    vga_print((struct point){str_line_middle(strlen("WWWOO     OOOWOOO                 OdOWOOO     OOWWWWW")), 59},  MAGENTA, "WWWOO     OOOWOOO                 OdOWOOO     OOWWWWW");
    vga_print((struct point){str_line_middle(strlen("WWOO     OONWOO                     OOWNdO     OOWWWW")), 68},  MAGENTA, "WWOO     OONWOO                     OOWNdO     OOWWWW");
    vga_print((struct point){str_line_middle(strlen("WNO     OONWOO                       OOWNOO    OONWWW")), 77},  MAGENTA, "WNO     OONWOO                       OOWNOO    OONWWW");
    vga_print((struct point){str_line_middle(strlen("WOO     OOWOO                         OOWOO     OOMWW")), 86},  MAGENTA, "WOO     OOWOO                         OOWOO     OOMWW");
    vga_print((struct point){str_line_middle(strlen("WOO     OOMOO                         OOWOO     OOWWW")), 95},  MAGENTA, "WOO     OOMOO                         OOWOO     OOWWW");
    vga_print((struct point){str_line_middle(strlen("WOO     OOWNdO                       OOWWOO     ONMWO")), 104},  MAGENTA, "WOO     OOWNdO                       OOWWOO     ONMWO");
    vga_print((struct point){str_line_middle(strlen("WWOO     OOWOOO                     OdNWOO     OOWWWO")), 113},  MAGENTA, "WWOO     OOWOOO                     OdNWOO     OOWWWO");
    vga_print((struct point){str_line_middle(strlen("WWNOO     OOWNOO                  OOOWNOO     OdNMWWW")), 122},  MAGENTA, "WWNOO     OOWNOO                  OOOWNOO     OdNMWWW");
    vga_print((struct point){str_line_middle(strlen("WWWOOO     OOOWOOOO             OOONWOOO     OONWWWWW")), 131},  MAGENTA, "WWWOOO     OOOWOOOO             OOONWOOO     OONWWWWW");
    vga_print((struct point){str_line_middle(strlen("WWWWOdO      OOONWOOdOOOOOOOOOdOOWNOOO      OdNWWWWWW")), 140},  MAGENTA, "WWWWOdO      OOONWOOdOOOOOOOOOdOOWNOOO      OdNWWWWWW");
    vga_print((struct point){str_line_middle(strlen("WWWWWNOOO      OOOOOOWWNNNNWWNOOOOOO      OOOWWWWWWWW")), 149},  MAGENTA, "WWWWWNOOO      OOOOOOWWNNNNWWNOOOOOO      OOOWWWWWWWW");
    vga_print((struct point){str_line_middle(strlen("WWWWWWWOOOO        OOdNWWWWMNdOO        OOONWWWWWWWWW")), 158},  MAGENTA, "WWWWWWWOOOO        OOdNWWWWMNdOO        OOONWWWWWWWWW");
    vga_print((struct point){str_line_middle(strlen("WWWWWWWWWWWWOOOOOO   OOMWWWWOO   OOOOOOWWWWWMWWWWWWWW")), 167},  MAGENTA, "WWWWWWWWWWWWOOOOOO   OOMWWWWOO   OOOOOOWWWWWMWWWWWWWW");
    vga_print((struct point){str_line_middle(strlen("WWWWWWWWWWWWWWWNOOOOOONWWWWWNOOdOOONWWWWWWWWWWWWWWWWW")), 176},  MAGENTA, "WWWWWWWWWWWWWWWNOOOOOONWWWWWNOOdOOONWWWWWWWWWWWWWWWWW");
    delay();
    vga_clear(BACKGROUND);
    gen_random_a();
    uint32_t rand_gen[15];
    for(uint32_t i=0;i<15;i++)
    {
        rand_gen[i] = myrand();
    }
    for(uint32_t i=0;i<15;i++)
    {
        for(uint32_t j=0;j<15;j++)
        {
            get_matrix[i] += (my_matrix[i*15+j] * rand_gen[j]) & (0xffff);
            get_matrix[i] = get_matrix[i] & 0xffff;
            vga_clear(BACKGROUND);
            vga_print((struct point){str_line_middle(strlen("GETFLAG OPERATING SYSTEM")), 5},  MAGENTA, "GETFLAG OPERATING SYSTEM");
            vga_print((struct point){0, 15},  MAGENTA, "OPERATING SYSTEM USE AI TECH");
            vga_print((struct point){0, 25},  MAGENTA, "SETTING A RANDOM FLAG SEED");
            vga_print((struct point){0, 35},  RED, "CHECKED YOU ARE PLAYING USTC HACKERGAME");
            vga_print((struct point){0, 45},  MAGENTA, "LET ME COMPUTE FLAG FOR YOU");
            vga_print((struct point){0, 55},  MAGENTA, "IF I FIND THE FLAG I WILL PRINT IT");
            for(short k=0; k<0xff;k++)
            {
                vga_print((struct point){0, 65},  RED, "COMPUTING PLEASE WAIT");
                usleep(800);
                vga_print((struct point){0, 65},  BLACK, "COMPUTING PLEASE WAIT");
                usleep(800);
            }
        }
    }
    vga_clear(BACKGROUND);
    vga_print((struct point){str_line_middle(strlen("GETFLAG OPERATING SYSTEM")), 5},  MAGENTA, "GETFLAG OPERATING SYSTEM");
    vga_print((struct point){0, 15},  MAGENTA, "FOUND A SOLUTION");
    vga_print((struct point){0, 25},  MAGENTA, "FLAG IS IN PRINTABLE FORMAT");
    vga_print((struct point){0, 35},  MAGENTA, "THE SYSTEM MAY GET WRONG SEED");
    vga_print((struct point){0, 45},  MAGENTA, "YOU SHOULD RESET IT");
    for(int i=0; i < 0xff; i++)
    {
        for(int j=0; j < 0xa0; j++)
        {

        }
    }
    delay();
    vga_off();
    // 187 49114 12533 39320 44039 25566 22160 10990 15801 27249 45757 55153 58050 7065 14228 
    // printl(get_matrix[0]);
    // printl(get_matrix[1]);
    // printl(get_matrix[2]);
    // printl(get_matrix[3]);
    // printl(get_matrix[4]);
    // printl(get_matrix[5]);
    // printl(get_matrix[6]);
    // printl(get_matrix[7]);
    // printl(get_matrix[8]);
    // printl(get_matrix[9]);
    // printl(get_matrix[10]);
    // printl(get_matrix[11]);
    // printl(get_matrix[12]);
    // printl(get_matrix[13]);
    // printl(get_matrix[14]);
    char out[40];
    
    out[30] = '$';
    out[31] = '$';
    out[32] = '$';
    out[33] = '$';
    print("\nYOU SHOULD CHECK PRINT OUT STRING ASCII$$");
    print("\nDOS ONLY PRINT UPPERCASE LETTERS$$");
    print("\n$$$$");
    unsigned short aim[30]={221, 49078, 12436, 39423, 44156, 25529, 22179, 10906, 15839, 27165, 45705, 55062, 58013, 7081, 14308, 136, 49064, 12481, 39404, 44086, 25520, 22263, 10929, 15818, 27144, 45774, 55045, 58097, 7156, 14313};
    for(short i=0; i<30;i++)
    {
        out[i] = (char)(aim[i] ^ get_matrix[i%15]);
    }
    print(out);
    return 0;
}
