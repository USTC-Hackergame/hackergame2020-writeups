# 超基础的数理模拟器

- 题目分类：general

- 题目分值：200

这一切的一切，还要从 Hackergame 2020 群说起。

不知是从什么时候，也许是上一次 Hackergame，或是更早，Hackergame 2020 群里的科气逐渐变得浓厚起来。 等到真正引起管理员注意时，上千人的群已经完全沦为了菜市场。 群里充斥着各式各样的卖菜声，比如 "tql"，"wtcl"，"sdl, wsl"，"orz"，"ddw"，各式各样的卖弱表情包交相辉映。 再加上群内复读机和正常人的比例严重失调，致使事态进一步恶化，场面一度无法控制。

在管理员和其余正常群友的齐心协力之下，此类现象在群内的出现频率最终显著下降。 但不幸的是，由于其他群的群主警惕不足，或是管理不慎(某大群群主甚至大肆宣扬 "科气 is fake"，听说最近连自己也未能幸免科了起来，也不知还能不能继续当选下一任群主)，每天仍然有许多群友在花式卖弱，而一些心理素质较差的群友也因此永远地退出了群聊。

各大水群的诸多龙王联合起来，研究多月之后，终于找到了此次事件的罪魁祸首: 那位身处大洋彼岸，就读于 UCB，不可提及姓名的老学长。而他的根本目的，就是试图利用同学们充满科气的卖弱行为，在如今废理兴工已经式微的科大，再次掀起反思数理基础教育的思想浪潮。 故而本次事件被命名为: FLXG-20。

为了应对那位学长的所作所为，我们在 Hackergame 2020 的网站上部署了一项超基础的数理模拟器。 作为一名数理基础扎实的同学，你一定能够轻松通过模拟器的测试吧。

[打开/下载题目](http://202.38.93.111:10190/login?token={token})

---

这是一道简单的检查数理基础扎实与否的题目，网站会随机生成定积分的式子供选手计算，如果能答对 400 题即可拿到 flag。

对于数理基础扎实的同学，你们通过口算定积分可以很轻松拿到 flag。

但是，如果你们的数理基础不够扎实，有毅力的同学也可以将每一道题都输入 CASIO 计算器，重复 400 遍即可达成条件。

对于没有 CASIO 计算器以及 Mathematica 等计算软件的同学，你们可以使用中国科技大学大雾实验专用坐标纸，在上面精准描绘之后数格点个数，不过由于本题精度要求较高，所以可能比较废纸。

对于那些数理基础太不扎实的计院同学，你们可以考虑写出数理基础足够扎实的 python 代码，代替你们进行测试：

```python
# pip3 install sympy antlr4-python3-runtime
import requests
from sympy import Integral, Symbol, E, latex
from sympy.parsing.latex import parse_latex
from urllib.parse import quote_plus
# from IPython.core.display import display, HTML

e = Symbol('e')
x = Symbol('x')

token = 'REDACTED' # Use your own token here
s = requests.session()
s.get(f'http://202.38.93.111:10190/login?token={quote_plus(token)}')
t = s.get('http://202.38.93.111:10190/').text
num = 400

while num > 1:
    num = t[t.find('<h1 class="cover-heading">')+26:t.find('</h1>')]
    num = int(num.split(' ')[1])
    print(num)
    m = t[t.find('<p> $')+5:t.find('{d x}$</p>')]

    # display(HTML(f"${m}$"))

    lu = m.split(' ')[0]
    lower = lu[6:lu.find('^')-1]
    lower = parse_latex(lower).n(20)
    upper = lu[lu.find('^')+2:-1]
    upper = parse_latex(upper).n(20)

    m = ' '.join(m.split(' ')[1:])
    m = m.replace(r'\right)', ')').replace(r'\left(', '(').replace(r'\,', '')
    m = parse_latex(m).subs(e,E)

    # display(HTML(f"${latex(m)}$"))

    ans = Integral(m, (x, lower, upper)).n(10)
    t = s.post('http://202.38.93.111:10190/submit', data={'ans':str(ans)}).text

print(t)
```