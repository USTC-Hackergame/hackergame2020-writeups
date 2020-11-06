# 超精巧的数字论证器

写一个简单的搜索算法可以解决数字较小的情况。

但是稍作尝试就会发现，当给定的数字较大时（例如 `100000`），就很难用表达式凑出接近这个大小的值。

稍作分析可以发现，这是因为所有给定的二元运算符一般都会使表达值的值变小，也就是说 `a+b a-b a*b a/b a%b a^b a&b a|b` 不会比 `ab` （不插入二元运算符）的值更大。所以，如果不使用一元运算符，表达式能凑出的最大值就是 `114514`，其次就是 `114*514=58596`。它们之间的值都不能被凑出来。由于需要连续答对 32 题才能获得 flag，所以必须解决这些情况。

那么突破口显然就在一元运算符 `+-~` 了。`+` 运算符显然没有用处，考虑 `-` 和 `~` 即可。

稍作研究就可以发现一个性质：`-~x=x+1` 对于任意 `x` 都成立。**这个性质与计算机中有符号整数的二进制补码表示有关。**

一元运算符可以不断嵌套。一个朴素的方法就是嵌套 `-~` 来不断地将表达式的值增加 1（反过来 `~-` 可以减少 1），最终得到目标值，但这样的话表达式就太长了，无法符合题目要求。

表达式中有 6 个数字，要好好利用它们才行。一个办法就是按照十进制的方式来凑，即 `given_number = (((((((0+a)*10+b)*10+c)*10+d)*10)+e)*10)+f` ，其中 `a b c d e f` 为 0 到 9 之间的整数。表达式中的值 `0 10 10 10 10 10` 可以分别利用 `1 1 4 5 1 4` 与嵌套 `~-` 来凑出，而 `+a +b +c +d +e +f` 可以直接利用嵌套 `~-` 来实现（不需要使用其它数字）。这样表达式就可以符合标准，而且长度不会超过限制了。

解题脚本（需要安装 pwntools）：

```python
#!/usr/bin/env python3


import pwn


def getans(number):
    jz = 10
    s = []
    e = "114514"
    for c in e[:1]:
        s.append("~-" * (int(c)) + c)  # value is zero
    for c in e[1:]:
        s.append("-~" * (jz - int(c)) + c)  # value is jz
    ans = ""
    for i in range(len(e)):
        digit = (number // (jz ** (len(e) - 1 - i))) % jz
        ans = "(" + ans + "*" + s[i] + ")" if i > 0 else s[i]
        ans = "-~" * digit + ans
    return ans


conn = pwn.remote('202.38.93.111', 10241)  # connect to the server
token = open('token', 'r').read()  # read the token
conn.sendlineafter('Please input your token:', token)  # send the token

for _ in range(32):
    number = int(conn.recvuntil('=').decode('utf-8').split()[-2])  # get the number
    ans = getans(number)  # calculate the answer
    conn.sendline(ans)  # send the answer
    print(str(number) + ' = ' + ans + '   ' + conn.recvline().decode('utf-8').strip())  # print the result

conn.interactive()  # print the flag
```

