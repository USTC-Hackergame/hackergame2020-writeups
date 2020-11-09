

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

def main():
    lines = open("/tmp/am").readlines()
    data: list[tuple] = []
    for line in lines:
        l = line.strip("\n").split("\t")
        data.append((l[0], int(l[1])))
    grand_total = 0
    for c, n in data:
        grand_total += convert(c) * n
    print(grand_total)

if __name__ == '__main__':
    main()