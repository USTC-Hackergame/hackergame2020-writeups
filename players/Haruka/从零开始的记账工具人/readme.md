# 从零开始的记账工具人

下载之后发现 xlsx 的内容果然都是中文大写数字金额，但因为窝懒，所以还是先上网搜了一下有没有现成的 python 代码能处理的。

……但搜了一圈只搜到了处理中文大写数字的，没有找到现成的能处理 `角` 和 `分` 的代码。

Fine，我自己写就是了！反正就是个字符串处理！

于是快速糊了一个金额转换函数：

```py
cn_num = list(" 壹贰叁肆伍陆柒捌玖")
cn_unit = {
    "佰": 100,
    "拾": 10,
    "元": 1,
    "角": 0.1,
    "分": 0.01,
}

def convert(cn: str):
    idx = 0
    amount = 0
    while idx < len(cn):
        ch = cn[idx]
        if ch in cn_unit.keys():
            if cn_unit[ch] <= 1:
                print("Incorrect unit sequence: %s %d" % (cn, idx))
            amount += cn_unit[ch]
            idx += 1
            if cn[idx] == "元":
                idx += 1
        elif ch in cn_num:
            num = cn_num.index(ch)
            ch_unit = cn[idx + 1]
            if ch_unit not in cn_unit.keys():
                print("Incorrect unit character: %s %d" % (cn, idx))
            amount += num * cn_unit[ch_unit]
            idx += 2
            if idx < len(cn) and cn[idx] == "元":
                idx += 1
        elif ch == "零":
            idx += 1
        elif ch == "整":
            break
        else:
            print("Unrecognized character: %s %d" % (cn, idx))
            idx += 1
    return amount
```
     
虽然其实不太好看，但总之 it works。于是只需要把每行内容提取出来然后塞进来处理就可以了。

……但我也懒得再找东西 parse xlsx。于是直接一把梭！

Excel 全选！复制！新建文本文件！粘贴！

然后把文本文件喂给 python 程序就好了。Excel 直接复制到文本文件会自动变成 TSV 格式，所以非常好处理。

最终的完整代码在[这里](cn_num.py)。

