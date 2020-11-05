import re

def to_upper(s):
    r = re.compile('[fF][lL][aA][gG]')
    if r.match(s):
        print('how dare you')
    elif s.upper() == 'FLAG':
        print('yes, I will give you the flag')
        print(open('/flag1').read())
    else:
        print('%s' % s.upper())

def to_utf8(s):
    r = re.compile('[fF][lL][aA][gG]')
    s = s.encode() # make it bytes
    if r.match(s.decode()):
        print('how dare you')
    elif s.decode('utf-7') == 'flag':
        print('yes, I will give you the flag')
        print(open('/flag2').read())
    else:
        print('%s' % s.decode('utf-7'))

def main():
    print('Welcome to the best string tool here!')
    print('Brought to you by 233 PROUDLY')
    print('')
    print('Which tool do you want?')
    print('1. Convert my string to UPPERCASE!!')
    print('2. Convert my UTF-7 string to UTF-8!!')
    choice = input()
    if choice[0] == '1':
        print('Welcome to the capitalizer tool, please input your string: ')
        to_upper(input())
    elif choice[0] == '2':
        print('Welcome to the UTF-7->UTF-8 tool, please input your string: ')
        to_utf8(input())
    else:
        print('I am confused, madam')

main()
