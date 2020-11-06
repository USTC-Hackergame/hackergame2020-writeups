from flask import Flask
from flask import request
app = Flask(__name__)

x = var('x')
y = var('y')

half1 = [log(x), sqrt(x)] # x >= 1
half2 = [x/y, y/x] # y > 0 and y is int and x >= 1
full1 = [e^x, sin(x), cos(x), sinh(x), cosh(x), arctan(x)]
full2 = [x+y, x+y, x*y, x-y]

def gen_f(depth=0):
    if (randint(0,2) != 0 and depth < 4) or depth < 2:
        return choice(full2)(x=gen_f(depth+1),y=gen_f(depth+1))
    elif (randint(0,2) != 0 and depth < 4):
        return choice(full1)(x=gen_f(depth+1))
    elif randint(0,2) != 0:
        return choice(half1)
    else:
        return choice(half2)(y=randint(1,4))

def gen_q():
    while True:
        f = gen_f()
        if f(x=1) == f(x=2) and f(x=2) == f(x=3):
            continue
        l = [QQ(randint(1,10))/QQ(randint(1,5)), QQ(randint(1,10))/QQ(randint(1,5))]
        if l[0] == l[1]:
            continue
        l.sort()
        fint = f.integral(x,l[0],l[1],hold=True)
        result, eps = numerical_integral(f,l[0],l[1])
        if abs(result) < 100000 and eps < 1e-7:
            break

    return (result, latex(fint).replace('log', 'ln'))

@app.route('/')
def gen():
    try:
        times = int(request.args.get('times'))
    except:
        times = 1
    ret = ''
    for i in range(times):
        r, s = gen_q()
        ret += str(r) + '\n' + s + '\n'
    return ret

if __name__ == '__main__':
    app.run(host='0.0.0.0')