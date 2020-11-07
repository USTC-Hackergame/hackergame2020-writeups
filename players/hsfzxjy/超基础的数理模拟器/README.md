# 超基础的数理模拟器

由于学过符号计算软件，本人首先想到用 Mathematica 去算积分，绕了点弯路，但还是可做的。以下给出代码。其中有几个要点：

 1. Mathematica 的 `ToExpression` 转换后的表达式是 `Integrate[...]` 也即符号积分，此时有可能算出奇怪的答案（比如复数解）。此时应该将 `Integrate` 替换为 `NIntegrate`。
 2. 其他一些替换，如把自然对数底 `e` 换成 `E`；最后的 `{d x}` 换成 `dx`；`\` 换成 `\\`；被积函数要用 `{}` 括起来。

偶尔会有几个积分算不出来，但概率不大。半小时左右能拿到 flag。

```python
import re
import pexpect
import requests


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Referer": "http://202.38.93.111:10190/",
}

s = requests.session()
s.cookies.clear()

address = "http://202.38.93.111:10190/"

tex_pattern = re.compile(
    r"(?P<progress>\d+)\s*题[.\s\S]+<p>\s*\$(?P<expr>.+)\$\s*</p>", re.M | re.X | re.U,
)
body_pattern = re.compile(r"(^[^\s]+\s)(?P<body>.*)\\")


def process_expr(expr: str):
    expr = expr.replace("{d x}", "dx")
    expr = re.sub(r"\be\b", "E", expr)
    expr = body_pattern.sub(r"\g<1>(\g<body>)\\", expr)
    expr = expr.replace("\\", "\\\\")
    return expr


def get_code(expr: str):
    return f'ToExpression["{expr}",TeXForm,Hold]/.Integrate->NIntegrate//ReleaseHold'


def next_probem(ans=""):
    if ans:
        response = s.post(address + "/submit", data=dict(ans=ans))
    else:
        response = s.get(address)
    print(response.text)
    matched = tex_pattern.search(response.text)
    expr = matched.group("expr")
    progress = matched.group("progress")
    expr = process_expr(expr)
    code = get_code(expr)
    p = pexpect.spawn("wolframscript", ["-code", code])
    p.wait()
    if p.exitstatus != 0:
        return "", progress
    try:
        answer = "{:.6f}".format(float(p.read().decode().strip()))
    except ValueError:
        return "", progress
    return answer, progress


ans = ""
while True:
    ans, round = next_probem(ans)
    print(ans, round)
    if round == 0:
        break
```