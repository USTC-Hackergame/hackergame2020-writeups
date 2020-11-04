import subprocess
import hashlib

if __name__ == "__main__":
    code = input("Your one line python code to exec(): ")
    print()
    if not code:
        print("Code must not be empty")
        exit(-1)
    p = subprocess.run(
        ["su", "nobody", "-s", "/bin/bash", "-c", "/usr/local/bin/python3 /runner.py"],
        input=code.encode(),
        stdout=subprocess.PIPE,
    )

    if p.returncode != 0:
        print()
        print("Your code did not run successfully")
        exit(-1)

    output = p.stdout.decode()

    print("Your code is:")
    print(repr(code))
    print()
    print("Output of your code is:")
    print(repr(output))
    print()

    print("Checking reversed(code) == output")
    if code[::-1] == output:
        print(open("/root/flag1").read())
    else:
        print("Failed!")
    print()

    print("Checking sha256(code) == output")
    if hashlib.sha256(code.encode()).hexdigest() == output:
        print(open("/root/flag2").read())
    else:
        print("Failed!")
