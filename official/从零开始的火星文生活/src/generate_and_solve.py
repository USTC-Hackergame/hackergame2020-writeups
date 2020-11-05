  
#全角->半角
def DBC2SBC(input_string):
    ret_string = ""
    for uchar in input_string:
        char_code = ord(uchar)
        if char_code == 0x3000:
            char_code = 0x0020
        else:
            char_code -= 0xfee0
        if not (0x0021 <= char_code and char_code <= 0x7e):
            ret_string += uchar
        else:
            ret_string += chr(char_code)
    return ret_string

#半角->全角
def SBC2DBC(input_string):
    ret_string = ""
    for uchar in input_string:
        char_code = ord(uchar)
        if char_code == 0x0020:
            char_code = 0x3000
        if not (0x0021 <= char_code and char_code <= 0x7e):
            ret_string += uchar
        else:
            char_code += 0xfee0
            ret_string += chr(char_code)
    return ret_string

def generate(message):
    dec_message=SBC2DBC(message)
    output=dec_message.encode('gbk').decode("iso-8859-1").encode('UTF-8').decode('gbk')
    return output

def solve(message):
    answer=DBC2SBC(message.encode("gbk").decode("UTF-8").encode("iso-8859-1").decode('gbk'))
    return answer

target="""
我攻破了 Hackergame 的服务器，偷到了它们的 flag，现在我把 flag 发给你：
flag{H4v3_FuN_w1Th_3nc0d1ng_4Nd_d3c0D1nG_9qD2R8hs}
快去比赛平台提交吧！
不要再把这份信息转发给其他人了，要是被发现就糟糕了！
"""


fout=open("files/gibberish_message.txt","w",encoding="UTF-8",errors='replace')
fout.write(generate(target))
fout.close()

fin=open("files/gibberish_message.txt","r",encoding="UTF-8",errors='replace')
source=fin.read()
answer=solve(source)
assert(DBC2SBC(target)==answer)
print(answer)