#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <assert.h>

#define EMPTY 0
#define BLACK 1
#define WHITE 2
#ifdef EXAMPLE
// Send payload to server to get flag plz
#define FLAG "\x76\x43\x49\x4C\x09\x5A\x4A\x55" \
             "\x41\x41\x4E\x54\x11\x46\x5C\x14" \
             "\x46\x53\x45\x4E\x5C\x48\x1B\x48" \
             "\x52\x1E\x58\x25\x35\x62\x25\x28" \
             "\x24\x21\x67\x38\x25\x30"
#else
// flag{easy_gamE_but_can_u_get_my_shel1}
#define FLAG "\x43\x4A\x46\x4F\x52\x4F\x4A\x5F" \
             "\x54\x71\x48\x51\x5C\x77\x6C\x56" \
             "\x40\x42\x68\x5B\x58\x54\x64\x49" \
             "\x62\x59\x5A\x34\x1E\x2F\x3A\x1B" \
             "\x36\x2E\x22\x24\x78\x37"
#endif

#define COMPUTER BLACK
#define HUMAN WHITE

#define MIN_SCORE -100

char flag[] = FLAG;
int board[3][3] = {};

void flag_decode(void) {
    for (int i = 0; flag[i] != '\0'; i++) {
        flag[i] ^= (i + 23333);
    }
}

int check(void) {
    for (int i = 0; i < 3; i++) {
        if (board[i][0] == board[i][1] && board[i][1] == board[i][2] && board[i][0] != EMPTY) {
            return board[i][0];
        }
        if (board[0][i] == board[1][i] && board[1][i] == board[2][i] && board[0][i] != EMPTY) {
            return board[0][i];
        }
    }
    if (board[0][0] == board[1][1] && board[1][1] == board[2][2] && board[0][0] != EMPTY) {
        return board[0][0];
    }
    if (board[0][2] == board[1][1] && board[1][1] == board[2][0] && board[0][2] != EMPTY) {
        return board[0][2];
    }
    return false;
}

bool full(void) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == EMPTY) {
                return false;
            }
        }
    }
    return true;
}

void print(void) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            char out = '_';
            if (board[i][j] == WHITE) {
                out = 'X';
            } else if (board[i][j] == BLACK) {
                out = 'O';
            } else if (board[i][j] != EMPTY) {
                out = '?';  // well if you see this something may be wrong.
            }
            printf("%c", out);
        }
        puts("");
    }
}

int opp(int p) {
    if (p == BLACK)
        return WHITE;
    else if (p == WHITE)
        return BLACK;
    assert(0);
}

int minimax(int player) {
    int winColor = check();
    if (winColor != EMPTY) {
        return winColor == player ? 1 : -1;
    }

    int movex = -1, movey = -1;
    int max_score = MIN_SCORE;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == EMPTY) {
                board[i][j] = player;
                int score = -minimax(opp(player));
                if (score > max_score) {
                    max_score = score;
                    movex = i; movey = j;
                }
                board[i][j] = EMPTY;
            }
        }
    }
    if (movex == -1) {
        return 0;
    }
    return max_score;
}

void ai(int *x, int *y) {
    // Make sure that human cannot win
    // I heard that there's an algorithm named "Minimax"
    int movex = -1, movey = -1;
    int max_score = MIN_SCORE;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == EMPTY) {
                board[i][j] = COMPUTER;
                int score = -minimax(HUMAN);
                if (score > max_score) {
                    max_score = score;
                    movex = i; movey = j;
                }
                board[i][j] = EMPTY;
            }
        }
    }
    *x = movex;
    *y = movey;
}

int main(void) {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);

    bool success = false;  // human wins?
    char input[128] = {};  // input is large and it will be ok.

    puts("Welcome to Tic Tac Toe! Computer first!");
    puts("You're 'X' and I'm 'O'!");
    while (!success) {
        // computer: BLACK
        int x, y;
        puts("Now computer goes!");
        ai(&x, &y);
        board[x][y] = BLACK;
        print();
        if (check()) {
            success = false;
            break;
        }
        if (full()) {
            break;
        }
        puts("Now human goes!");
        // human: WHITE

        // example input: (0,1)
        while (true) {
            printf("Your turn. Input like (x,y), such as (0,1): ");
            gets(input);
            x = input[1] - '0';
            y = input[3] - '0';
            printf("You wanna put X on (%d,%d)...\n", x, y);
            if (!(x >= 0 && x < 3 && y >= 0 && y < 3)) {
                puts("Wrong input! Please try again!");
                continue;
            }
            if (board[x][y] != EMPTY) {
                puts("This pos has already been occupied!");
                continue;
            }
            break;
        }
        board[x][y] = WHITE;
        print();
        if (check()) {
            success = true;
            break;
        }
        if (full()) {
            break;
        }
    }
    if (success) {
        puts("What? You win! Here is your flag:");
        flag_decode();
        puts(flag);
    } else {
        puts("You failed! See you next time~");
    }
    return 0;
}