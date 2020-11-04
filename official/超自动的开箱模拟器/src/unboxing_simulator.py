from collections import deque
from random import SystemRandom


class BF:
    def __init__(self, code):
        self.code = code
        self.output = deque()
        self.input = deque()
        self.data = [0]
        self.codeptr = 0
        self.dataptr = 0
        self.generate_map()

    def generate_map(self):
        self.map = {}
        stack = []
        for i, op in enumerate(self.code):
            if op == "[":
                stack.append(i)
            elif op == "]":
                if not stack:
                    print("Error: Brackets not matching")
                    exit(-1)
                pos = stack.pop()
                self.map[pos] = i
                self.map[i] = pos
        if stack:
            print("Error: Brackets not matching")
            exit(-1)

    def step(self):
        op = self.code[self.codeptr]
        if op == ">":
            self.dataptr += 1
            if self.dataptr == len(self.data):
                self.data.append(0)
        elif op == "<":
            if self.dataptr:
                self.dataptr -= 1
        elif op == "+":
            self.data[self.dataptr] += 1
            self.data[self.dataptr] %= 256
        elif op == "-":
            self.data[self.dataptr] -= 1
            self.data[self.dataptr] %= 256
        elif op == "[":
            if self.data[self.dataptr] == 0:
                self.codeptr = self.map[self.codeptr]
        elif op == "]":
            if self.data[self.dataptr] != 0:
                self.codeptr = self.map[self.codeptr]
        elif op == ".":
            self.output.append(self.data[self.dataptr])
        elif op == ",":
            if not self.input:
                print("Error: No input")
                exit(-1)
            self.data[self.dataptr] = self.input.popleft()
        self.codeptr += 1

    def run_till_output(self):
        while self.codeptr < len(self.code):
            self.step()
            if self.output:
                return self.output.popleft()
        return None


class Game:
    def __init__(self, nboxes, nguess):
        self.nboxes = nboxes
        self.nguess = nguess
        rnd = SystemRandom()
        self.boxes = list(range(1, nboxes + 1))
        rnd.shuffle(self.boxes)

    def play_one_round(self, target, code):
        bf = BF(code)
        bf.input.append(target)
        box_key = 0
        guesses = 0
        while guesses < self.nguess:
            out = bf.run_till_output()
            if out is None:
                print("Error: No enough output after BF ended")
                exit(-1)
            if out == 1:  # move left
                if box_key > 0:
                    box_key -= 1
            elif out == 2:  # move right
                if box_key < self.nboxes - 1:
                    box_key += 1
            elif out == 3:  # open current box
                guesses += 1
                box_value = self.boxes[box_key]
                print(f"- Guess {guesses}/{self.nguess}: {box_key}->{box_value}")
                if box_value == target:
                    print("Target found")
                    return True
                bf.input.append(box_value)
        print(f"Target not found after {self.nguess} guesses")
        return False

    def play(self, code):
        for i in range(1, self.nboxes + 1):
            print(f"Running round {i}/{self.nboxes}, target = {i}")
            if not self.play_one_round(i, code):
                return False
        return True


if __name__ == "__main__":
    code = input("Your unboxing BF code: ")
    game = Game(128, 64)
    if game.play(code):
        print("You win")
        print(open("flag").read())
    else:
        print("You lose")
