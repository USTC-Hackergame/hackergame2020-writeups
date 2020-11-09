# 超基础的数理模拟器

![image](https://user-images.githubusercontent.com/861659/98481257-58e95180-223c-11eb-8aa6-4fad8170743c.png)

（掀桌

（我选择![image](https://user-images.githubusercontent.com/861659/98481306-b087bd00-223c-11eb-9d36-8a749d7d43ea.png)

既然这题这样，那看来应该是需要有什么方式用代码来算结果了。作为 python 用户，自然想到了 sympy 来处理这个东西。

网页上渲染这玩意基本都是用的 MathJax，恰好这道题的渲染输入就用了 TeX，而 sympy 正好支持 TeX 输入，这样就可以直接在代码里下载网页 - sympy 输入 - 计算 - 提交结果一条龙，岂不美哉.jpg

于是问题再次转变成了分析网页上的请求然后代码模拟了。和狗狗银行不一样的是，这道题看上去所有信息都存在了 `session` cookie 里 - 包括当前的题和剩余题目数量，因此在每次请求之后都需要处理 `Set-Cookie`（或者使用请求库的 cookie 存储一类的玩意）。

因为网页格式非常固定，所以我还是用了禁忌的 regex 处理 html 的方式。H̸̡̪̯ͨ͊̽̅̾̎Ȩ̬̩̾͛ͪ̈́̀́͘ ̶̧̨̱̹̭̯ͧ̾ͬC̷̙̲̝͖ͭ̏ͥͮ͟Oͮ͏̮̪̝͍M̲̖͊̒ͪͩͬ̚̚͜Ȇ̴̟̟͙̞ͩ͌͝S̨̥̫͎̭ͯ̿̔̀ͅ

最终代码：

```py
import requests
import re
import pickle

from sympy.parsing.latex import parse_latex
from sympy.core.numbers import Float

cookies = {"session": "session"}

def main():
    global cookies
    try:
        cookies = pickle.load(open("/tmp/session", "rb"))
    except:
        pass
    while True:
        r = requests.get("http://202.38.93.111:10190/", cookies=cookies)
        if r.ok:
            cookies["session"] = r.headers["set-cookie"][8:]
            d = r.text
            left = re.findall(r'<h1 class="cover-heading"> (\d+) 题</h1>', d)
            if len(left) > 0:
                left = int(left[0])
                print(left)
            else:
                print(d)
                break
            tex = re.findall(r"<p> \$(.*)\$</p>", d)
            if len(tex) > 0:
                tex = tex[0].replace(r"\,", "").replace(r"\left", "").replace(r"\right", "")
                span = re.match(r"\\int_{.*}\^{.*?} ", tex).span(0)
                tex = tex[:span[1]] + "{" + tex[span[1]:] + "}"
            else:
                print(d)
                break
            i = parse_latex(tex)
            res = i.evalf(10)
            print(res)
            if isinstance(res, Float):
                r = requests.post("http://202.38.93.111:10190/submit", data={"ans": res}, cookies=cookies, allow_redirects=False)
                if r.ok:
                    cookies["session"] = r.headers["set-cookie"][8:]
                else:
                    print(r.status_code)
        pickle.dump(cookies, open("/tmp/session", "wb"))

if __name__ == '__main__':
    main()
```