# 自复读的复读机

## 解题思路

使用搜索引擎搜索“输出自己的程序”或者类似的词，可以查到这类程序叫做 Quine。可以很容易在网上查到很多 Python 3 的 Quine，例如：

`exec(s:='print("exec(s:=%r)"%s)')`

还有

`s='s=%r;print(s%%s)';print(s%s)`

等等。

这道题要求输出代码的逆序以及代码的哈希，我们可以修改上面的 Quine：

输出自己逆序的程序：`exec(s:='print(("exec(s:=%r)"%s)[::-1])')`（把 print 的内容用括号括起来然后逆序即可）

但这样提交之后有一个问题，就是输出比代码多了一个 `\n`，这是由于输入的代码结尾没有换行符而 `print` 输出的内容结尾会自带换行符，我们只需要让 `print` 不输出换行符，加一个 `,end=""` 即可。

对于第二问，我们把 print 的内容用 Python 自带的计算 sha256 的函数包起来即可。

## 答案

第一问（每行都是一个可能的构造）：

`exec(s:='print(("exec(s:=%r)"%s)[::-1],end="")')`

`s='s=%r;print((s%%s)[::-1],end="")';print((s%s)[::-1],end="")`

第二问（每行都是一个可能的构造）：

`exec(s:='print(__import__("hashlib").sha256(("exec(s:=%r)"%s).encode()).hexdigest(),end="")')`

`exec(s:='import hashlib;print(hashlib.sha256(("exec(s:=%r)"%s).encode()).hexdigest(),end="")')`

`import hashlib;s='import hashlib;s=%r;print(hashlib.sha256((s%%s).encode()).hexdigest(),end="")';print(hashlib.sha256((s%s).encode()).hexdigest(),end="")`

## 其他

要注意的是，这道题的程序是使用标准输入读入代码然后用 `exec()` 执行的，所以并不能使用 `print(open(__file__).read())` 之类输出自己源代码文件的方案。

你可以使用 `import os; os.system('ls')` 之类的代码来在服务器上任意执行命令，但是进程是以低权限运行的，这种方法不能读到 flag。

你也可以通过读取当前进程的内存来找到自己的源代码然后输出，理论上完全可行，但我没有实现，如果有选手做到了可以提 PR 来分享给大家。
