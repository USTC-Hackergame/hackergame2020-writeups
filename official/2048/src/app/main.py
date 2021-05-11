from flask import Flask
from flask import request, render_template, redirect, url_for, session, make_response

import OpenSSL
import base64


from secret import hg_dynamic_flag, secret_key

app = Flask(__name__)
app.secret_key = secret_key

with open("cert.pem") as f:
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())


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
        return redirect(url_for('index'))
    if session.get("token") is None:
        return make_response(render_template("error.html"), 403)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/getflxg', methods=['GET'])
def getflxg():
    if request.args.get('my_favorite_fruit') == 'banana':
        return hg_dynamic_flag(session['token'])
    else:
        return '还没有大成功，不能给你 flxg。'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=10005, debug=True)
