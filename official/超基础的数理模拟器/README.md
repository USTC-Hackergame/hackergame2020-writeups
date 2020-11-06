# 超基础的数理模拟器

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