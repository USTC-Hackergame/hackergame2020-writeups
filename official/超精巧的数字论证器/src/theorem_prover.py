import random


target = 114514
challenges = 32


def get_value(expr):
    for char in expr:
        if char not in "()+-*/%~&|^" + str(target):
            return False
    if "".join([char for char in expr if char in str(target)]) != str(target):
        return False
    if "**" in expr or "//" in expr or "()" in expr:
        return False
    expr = expr.replace("/", "//")
    try:
        v = eval(expr)
        assert type(v) == type(0)
    except:
        return False
    else:
        return v


for i in range(challenges):
    n = random.randint(1, min(target, 10**i))
    expr = input(("Challenge ({}/{}):   {} = ".format(i + 1, challenges, n))).strip()
    if len(expr) > 256:
        print("Too long!")
        print("Failed!")
        break
    v = get_value(expr)
    if v is False:
        print("Invalid expr!")
        print("Failed!")
        break
    else:
        if v == n:
            print("Q.E.D.")
        else:
            print("{} = {} (which is not {})".format(expr, v, n))
            print("Failed!")
            break
else:
    print("You finished all challenges!")
    print(open("flag").read())
