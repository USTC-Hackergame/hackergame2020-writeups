import numpy as np
from PIL import ImageFont, ImageDraw, Image
from matplotlib import pyplot as plt
import pathlib

import string
from random import SystemRandom
random = SystemRandom()

alphabet = sorted(string.digits + string.ascii_letters)

def img_generate(text):
    img = Image.new('RGB', (40 * len(text), 100), (255, 255, 255))
    # https://github.com/adobe-fonts/source-code-pro/raw/release/TTF/SourceCodePro-Light.ttf
    fontpath = pathlib.Path(__file__).parent.absolute().joinpath("SourceCodePro-Light.ttf")
    font = ImageFont.truetype(str(fontpath), 64)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, font = font, fill = (0,0,0,0))
    return img


def add_noise(draw, size):
    def get_random_xy(draw):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        return x, y
    
    def get_random_color():
        r = random.randint(0, 256)
        g = random.randint(0, 256)
        b = random.randint(0, 256)
        return r, g, b
    
    draw.line([get_random_xy(draw), get_random_xy(draw)], 
                get_random_color(), width=1)


def shuffle(img):
    pix = np.array(img)
    x, y, z = pix.shape
    t = pix.reshape(-1, z).tolist()
    random.shuffle(t)
    pix_shuffled = np.array(t, dtype=np.uint8).reshape(x, y, z)
    return Image.fromarray(pix_shuffled)


def generate_captcha(code, shuffle_mode=False):
    img = img_generate(code)
    draw = ImageDraw.Draw(img)
    for _ in range(10):
        add_noise(draw, size=img.size)

    if shuffle_mode:
        return shuffle(img)
    else:
        return img

if __name__ == "__main__":
    code = "".join([random.choice(alphabet) for _ in range(16)])
    print("Code:", code)

    img_orig = generate_captcha(code, shuffle_mode=False)
    img_orig.save('captcha.bmp')

    img_shuffled = generate_captcha(code, shuffle_mode=True)
    img_shuffled.save('captcha_shuffled.bmp')
