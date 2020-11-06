import os

level = int(input("Which level do you want to play (1/2/3)? "))
if level == 1:
    os.system("python3 -u MITM1.py")
elif level == 2:
    os.system("python3 -u MITM2.py")
elif level == 3:
    os.system("python3 -u MITM3.py")
else:
    print("Invalid input")
