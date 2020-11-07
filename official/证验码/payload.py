#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: captcha_payload.py

# STEP 0: pip3 install requests numpy matplotlib Pillow
# STEP 1: run `wget https://github.com/adobe-fonts/source-code-pro/raw/release/TTF/SourceCodePro-Light.ttf`
# STEP 2: download attachment `shuffle.py`
# STEP 3: fill in your `TOKEN`
# STEP 4: run `python3 payload.py`

BASE = "http://202.38.93.111:10150/"
TOKEN = "123:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

import requests
from io import BytesIO
from shuffle import *


def solve(img):
    
    def count_pix(img):
        pix = np.array(img)
        x, y, z = pix.shape

        cnt = np.zeros(256, dtype=np.int)

        for i in range(x):
            for j in range(y):
                if len(set(pix[i, j])) == 1:
                    # do not count noises
                    cnt[pix[i, j, 0]] += 1

        # ignore pure white
        return cnt[:-1]
    
    # char-pix matrix, shape: (62, 255)
    A = np.array([count_pix(img_generate(c)) for c in alphabet])
    
    # pix sum vector, shape: (255, )
    b = count_pix(img)
    
    # Solve A^T.x = b using least-squares method
    xf, *_ = np.linalg.lstsq(A.T, b, rcond=None)
    
    # number matrix, shape: (62, )
    x = xf.round().astype(np.int).tolist()
    
    return x


s = requests.Session()

r = s.get(BASE, params={'token': TOKEN}) # pass token
r = s.get(BASE + "captcha_shuffled.bmp") # request shuffled captcha
img = Image.open(BytesIO(r.content))     # load image data

x = solve(img)

# construct url parameters
url = "result?"
for idx, n in enumerate(x):
    url += "&r_{c}={n}".format(c=alphabet[idx], n=n)

r = s.get(BASE + url)
print(r.text)
