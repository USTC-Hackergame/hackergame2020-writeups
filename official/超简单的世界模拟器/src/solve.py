import random

MAP_SIZE = 50
CONTROL_SIZE = 15
STEP = 200
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

random.seed(2020)
while True:
    game = Game(MAP_SIZE, MAP_SIZE)
    for i in range(CONTROL_SIZE):
        for j in range(CONTROL_SIZE):
            game.map[i][j] = random.randrange(2)
    s = ''
    for line in game.map[:CONTROL_SIZE]:
        for i in line[:CONTROL_SIZE]:
            s += str(i)
        s += '\n'

    last = game.map
    for i in range(STEP):
        game.step()
        if game.map == last:
            break
        last = game.map

    cnt = 0
    for i, flag in enumerate(FLAGS):
        if all(not game.map[x][y] for x, y in flag_range(flag)):
            cnt += 1
    print("flags =", cnt)
    if cnt:
        print(s)
