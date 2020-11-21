这真的是我唯一可以拿的出手的了  
膜拜各位大佬

超精巧的数字论证器
=================
经过了长达一天的尝试，最终我将114514拆为114\*51\*4，然后使用-\~和\~-覆盖所有的数字  
理论上这个范围应该能更广  
```Python
def eq(s,i,n):
    if i < n:
        for i in range(n-i):
            s="~-"+s
    elif i>n:
        for i in range(i-n):
            s="-~"+s
    return s
while 1:
    i=int(input())
    s=""
    n=0
    if(i<0):
        exit(0)
    else:
        s="4"
        n=4
        t=round(i/114)
        t=round(t/51)
        s=eq(s,t,n)
        s="(51*"+s+")"
        n=t*51
        t=round(i/114)
        s=eq(s,t,n)
        s="(114*"+s+")"
        n=t*114
        s=eq(s,i,n)
        print(len(s))
        print(s)
```
