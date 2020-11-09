# 狗狗银行

打开网站，看了一下发现，这个利率根本赢不了嘛！

然后想到，难道这道题需要靠小数点四舍五入来套利息？

开了几张储蓄卡来回转账测试了一下，发现果然他在计算利息的时候是四舍五入到整数的，只要卡里有 167 的余额就可以得到 1 的利息（`167 * 0.003 = 0.501`）。但开始的 1000 资产全分到卡上也不够开，看来信用卡也能用类似的方式套到利息。

测试发现，一张信用卡的欠款直到 2099 都只收 10 的利息（`2099 * 0.005 = 10.495`），但是 2004 就可以提供 12 张储蓄卡每天 1 的利息（`167 * 12 = 2004`），这样每张信用卡就可以每天套到 2 的利息。但是利息导致欠款超过 2099 时利润空间就会缩小到 1，需要重新分布所有卡的金额。

我：qtmd，我直接开始就开上几百张信用卡不就行了

显然上百张没办法手工操作（累死了），于是问题转变成了写客户端实现网页操作而已。

整个程序的请求也很简单，只有 `/api/create` 办新卡和 `/api/transfer` 转账，直接 F12 看一会网络就能分析清楚了。

为了计算方便，开始开了 29 张信用卡，对应需要开 348 张储蓄卡（开始送的 1000 就放在那不管了），这样信用卡对应 id 是 2-30，储蓄卡是接下来的 31-378。然后只需要开上卡转账就行了，每天吃饭可以直接在网页上点点点观察（并且可以用 1000 的卡吃饭降低影响）。

…………结果 29 张卡还真的不够用，还没到 2000 就开始变穷了。

把数目换成 39, 468，重新跑了一次，终于够了，网页上可以直接看到 flag。

最终创建和转账的代码：

```py
import requests

cookie = {"session": "session"}
auth = {"Authorization": "Bearer token"}

create = "http://202.38.93.111:10100/api/create"
transfer = "http://202.38.93.111:10100/api/transfer"

def tr(fr, to, am):
    print("tr %d -> %d" % (fr, to))
    requests.post(transfer, json={"src": fr, "dst": to, "amount": am}, cookies=cookie, headers=auth)

def cr(ty):
    print("cr %s" % ty)
    requests.post(create, json={"type": ty}, cookies=cookie, headers=auth)


# 2-40 cr
# 41-508 de

for i in range(39):
    cr("credit")

for i in range(468):
    cr("debit")

for i in range(39):
    for j in range(12):
        tr(i + 2, 40 + 12 * i + j + 1, 167)

```

