# 证验码

首先我们来分析题目的设置：

- 正常提交验证码，提示信息是 shuffle 过后的，如果验证码正确，可以得到被 shuffle 之后的 flag；
- shuffle 模式提交验证码，验证码是 shuffle 过后的，随意提交，提示信息是正常顺序；
- 因为是选择字符数量，提交验证码的时候不需要字符顺序正确；
- 从题目附件脚本来看，产生验证码的全部信息都已知，包括字体、字符集、长度等；
- 验证码有 16 个字符，10 条彩色随机噪音；
- 附件使用的随机产生器都是 SystemRandom；

根据题意和以上设置可以推测：

- shuffle 模式下如果验证码正确，可以得到正常模式的 flag；
- 只需要还原有哪些字符，不用还原字符顺序（应该也没法还原）；
- 不用考虑随机数预测；

所以我们的任务就是：通过 shuffle 后的验证码图片还原其中的字符个数。

观察渲染生成的验证码中的文字，发现这些文字的像素值是均匀分布在黑色到白色间的，共有 256 种可能的取值，边缘处逐渐由黑变白，并不是只有纯黑和纯白，我们忽略纯白的那种取值，还剩下 255 种。

记 pix(x) 为字符 x 生成图片中像素值的统计向量（忽略白色，维度：255），我们可以得到以下恒等关系：

forall x, y, pix(x . y) = pix(x) + pix(y),

其中 `.` 为字符串连接，所以对于验证码来说，

pix(captcha) = sum(pix(c) for c in captcha) = sum(n(captcha, x) * pix(x) for x in alphabet),

其中 captcha 是验证码，alphabet 是字符集（共 62 个），n(captcha, x) 是某个字符在验证码中出现的次数。

如果我们把字符集中所有字符的 pix() 计算出，就可以排列成维度为 (62, 255) 的字体像素矩阵 A，其中 aij 代表第 i 个字符的图像有多少个像素值为 j 的像素。同时将 shuffle 后验证码整体统计得到的 pix() 计算出，记为维度为 255 的向量 b，那么我们想要求解的就是字符数量就是维度为 62 的向量 x = (n(captcha, 'a'), n(captcha, 'b'), ...)，并且有以下方程：

Ax = b,

啊这。这不是线性方程吗，还是个超定线性方程组，解就完事儿了。

## 噪音的处理

噪音使得上式不完全相等，不能应用一些精确求解办法。首先我们在统计 pix(captcha) 时忽略所有彩色的像素，由于彩色的噪声遮盖了部分字符，我们的 b 会比真实的 b_true 略小一点，这样得到的方程是：

Ax = b_true - noise,

其中 noise 为非负的噪音。

## 解线性方程的方法

由于噪音未知（是随机生成的）但是很小，对上式变形，用优化方法最小化噪音，求解 x* = argmin_x(noise^2) = argmin_x((Ax - b_true)^2) 即可。

有很多方法可以求解此式，下面给出一种使用最小二乘的参考方法。

```python
# char-pix matrix, shape: (62, 255)
A = np.array([count_pix(img_generate(c)) for c in alphabet])

# pix sum vector, shape: (255, )
b = count_pix(img)

# Solve A^T.x = b using least-squares method
xf, *_ = np.linalg.lstsq(A.T, b, rcond=None)

# number matrix, shape: (62, )
x = xf.round().astype(np.int).tolist()
```

## 其他做法

本题也可以用线性回归、神经网络等，直接拟合 pix(captcha) -> x 的映射关系，准确率足以通过本题。

## 完整程序

见 [payload.py](payload.py)。
