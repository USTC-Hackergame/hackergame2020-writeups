import time


MAP_SIZE = 50
CONTROL_SIZE = 15
STEP = 200
INTERVAL = 0.1
FLAGS = [(5, 45), (25, 45)]


def flag_range(flag):
    x, y = flag
    for i in range(2):
        for j in range(2):
            yield x + i, y + j


class Game:
    def __init__(self, W, H):
        self.W = W
        self.H = H
        self.map = [[0 for _ in range(W)] for _ in range(H)]

        for flag in FLAGS:
            for x, y in flag_range(flag):
                self.map[x][y] = 1

    def print(self):
        buf = ""
        for i in range(self.H):
            for j in range(self.W):
                flag = any((i, j) in flag_range(f) for f in FLAGS)
                if self.map[i][j]:
                    buf += "\x1b[48;5;0m"
                    buf += "\x1b[38;5;15m"
                else:
                    buf += "\x1b[48;5;15m"
                    buf += "\x1b[38;5;0m"
                if flag:
                    buf += "[]"
                else:
                    buf += "  "
                buf += "\x1b[0m"
            buf += "\n"
        return buf

    def step(self):
        new = [[0 for _ in range(self.W)] for _ in range(self.H)]
        for i in range(self.H):
            for j in range(self.W):
                cnt = 0
                for io in -1, 0, 1:
                    for jo in -1, 0, 1:
                        if 0 <= i + io < self.H:
                            if 0 <= j + jo < self.W:
                                if io != 0 or jo != 0:
                                    if self.map[i + io][j + jo]:
                                        cnt += 1
                if cnt == 3:
                    new[i][j] = 1
                elif cnt == 2:
                    new[i][j] = self.map[i][j]
                else:
                    new[i][j] = 0
        self.map = new


game = Game(50, 50)

print(game.print())

print(f"Your {CONTROL_SIZE}x{CONTROL_SIZE} 0/1 matrix at upper left corner: ")
for i in range(CONTROL_SIZE):
    line = input()
    if not line:
        break
    assert len(line) <= CONTROL_SIZE and set(line) <= {"0", "1"}
    for j in range(len(line)):
        game.map[i][j] = int(line[j])

print("\033c", end="")
print(game.print())
print("Let's begin...")
time.sleep(1)

for i in range(STEP):
    time.sleep(INTERVAL)
    game.step()
    buf = game.print()
    print("\033c", end="")
    print(i + 1)
    print(buf)

cnt = 0
for i, flag in enumerate(FLAGS):
    if all(not game.map[x][y] for x, y in flag_range(flag)):
        cnt += 1
if cnt == 1:
    print("You destroyed one block, flag 1:")
    print(open("flag1").read())
elif cnt == 2:
    print("You destroyed two blocks, flag 2:")
    print(open("flag2").read())
else:
    print("Flag block not destroyed")
