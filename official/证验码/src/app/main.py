from flask import Flask
from flask import request, session, redirect, url_for, render_template, make_response
from flask_session import Session
from io import BytesIO

import OpenSSL
import base64
import hashlib

with open("cert.pem") as f:
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())

from random import SystemRandom
random = SystemRandom()

from secret import secret_key, flag
from utils import generate_captcha, alphabet

app = Flask(__name__)
app.secret_key = secret_key
SESSION_TYPE = 'filesystem' # IMPORTANT!
SESSION_FILE_THRESHOLD = 2000
app.config.from_object(__name__)
Session(app)

@app.before_request
def check():
    if request.path.startswith('/static/'):
        return
    if request.args.get('token'):
        try:
            token = request.args.get('token')
            id, sig = token.split(":", 1)
            sig = base64.b64decode(sig, validate=True)
            OpenSSL.crypto.verify(cert, sig, id.encode(), "sha256")
            session['token'] = token
        except Exception:
            session['token'] = None
        return redirect(url_for('normal_view'))
    if session.get("token") is None:
        return make_response(render_template("error.html"), 403)


@app.template_filter('shuffle')
def shuffle(s, shuffle_mode=False):
    if shuffle_mode:
        t = list(s)
        random.shuffle(t)

        if type(s) is str:
            return "".join(t)
        else:
            return t
    else:
        return s


@app.route('/', methods=['GET'])
def normal_view():
    return render_template('index.html', alphabet=alphabet)


@app.route('/shuffle', methods=['GET'])
def shuffle_view():
    return render_template('index.html', alphabet=alphabet, shuffle_mode=True)


@app.route('/result', methods=['GET'])
def result():
    code = session.get('code')
    shuffle_mode = session.get('shuffle_mode') # TODO: avoid race condition!

    print(code)

    if code is None or shuffle_mode is None:
        return 'failed'

    # count user input
    user_cnt = dict()
    for c in alphabet:
        user_cnt[c] = 0
    
    for c in alphabet:
        r_c = request.args.get("r_" + c)
        if r_c:
            user_cnt[c] = int(r_c)

    # count answer
    answer_cnt = dict()
    for c in alphabet:
        answer_cnt[c] = 0

    for c in code:
        answer_cnt[c] += 1

    # DEBUG: construct right example
    ans = ""
    for c in answer_cnt:
        if answer_cnt[c]:
            ans += "&r_" + c + "=" + str(answer_cnt[c])
    print(ans)

    # compare answer & user input
    if all([user_cnt[c] == answer_cnt[c] for c in alphabet]):
        gotit = True
        msg = "验证通过，flag 为：" + flag % hashlib.sha256(('R40Md0M.5Huffl3'+session['token']).encode()).hexdigest()[:32]
        msg = shuffle(msg, shuffle_mode=not shuffle_mode)
    else:
        gotit = False
        msg = "验证没有通过，请重新尝试"
    
    return render_template('result.html', gotit=gotit, msg=msg, shuffle_mode=shuffle_mode)

@app.route('/captcha.bmp', methods=['GET'])
def captcha_bmp():
    code = "".join([random.choice(alphabet) for _ in range(16)])
    img = generate_captcha(code, shuffle_mode=False)
    temp = BytesIO()
    img.save(temp, format="bmp")

    session['code'] = code
    session['shuffle_mode'] = False
    
    response = make_response(temp.getvalue())
    response.headers.set('Content-Type', 'image/bmp')
    return response


@app.route('/captcha_shuffled.bmp', methods=['GET'])
def captcha_shuffled_bmp():
    code = "".join([random.choice(alphabet) for _ in range(16)])
    img = generate_captcha(code, shuffle_mode=True)
    temp = BytesIO()
    img.save(temp, format="bmp")
    
    session['code'] = code
    session['shuffle_mode'] = True

    response = make_response(temp.getvalue())
    response.headers.set('Content-Type', 'image/bmp')
    return response


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=10150, debug=True)
