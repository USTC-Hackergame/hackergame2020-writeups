import random
import os
import requests
import time

import OpenSSL
import base64
import hashlib

from functools import wraps

from flask import Flask, request, session, redirect, url_for, render_template, make_response
from encrypted_session import EncryptedSessionInterface

app = Flask(__name__, static_folder='static', static_url_path='', template_folder='templates')
app.secret_key = b"REDACTED"
app.config['SESSION_CRYPTO_KEY'] = b"REDACTED"
app.session_interface = EncryptedSessionInterface()

with open("cert.pem") as f:
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login')
def login():
    try:
        token = request.args.get('token')
        id, sig = token.split(":", 1)
        sig = base64.b64decode(sig, validate=True)
        OpenSSL.crypto.verify(cert, sig, id.encode(), "sha256")
        session['token'] = token
        session['score'] = 0
        session.pop('ans', None)
        return redirect(url_for('index'))
    except Exception:
        return make_response('''
        您尚未登录或登录 token 错误, 请使用 hackergame 网站上的题目链接访问
    ''', 403)

@app.route('/logout')
def logout():
    session.pop('token', None)
    session.pop('score', None)
    session.pop('ans', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    total = 400
    width = (session['score'] / float(total)) * 100
    if width >= 100:
        token = session['token']
        return f"flag{{S0lid_M4th_Phy_Foundation_{hashlib.sha256(('S01idF'+token).encode()).hexdigest()[:10]}}}"
    formula = requests.get("http://generator:5000").text.split('\n')
    session['ans'] = float(formula[0])
    #print(formula[0])
    result = session.pop('result', None)
    return make_response(render_template("index.html", remaining=total-session['score'], width=width, latex=formula[1], result=result))


@app.route('/submit', methods=['POST'])
@login_required
def submit():
    try:
        ans = request.form['ans']
        ans = float(ans)
        if abs(session['ans'] - ans) < 1e-6:
            session['score'] += 1
            session['result'] = "true"
        else:
            session['result'] = "false"
    except:
        pass
    session.pop('ans', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)