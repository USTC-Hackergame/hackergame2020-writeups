from io import BytesIO
from flask import Flask
from flask import request, render_template, redirect, url_for, session, make_response, send_file

import OpenSSL
import base64

import xlsxwriter
import io
import cn2an
import random

from secret import total_money, secret_key

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
    total = total_money(session['token'])
    file = io.BytesIO()
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, '单价')
    worksheet.write(0, 1, '数量')

    random.seed(session['token'])
    cut = set()
    while len(cut) < 999:
        n = random.randrange(1, total)
        cut.add(n)
    cut = [0] + sorted(cut) + [total]

    row = 1
    for start, end in zip(cut[:-1], cut[1:]):
        total_price = end - start
        price = total_price
        count = random.randrange(2, 11)
        if price % count == 0:
            price //= count
        else:
            count = 1
        assert count * price == total_price
        worksheet.write(row, 0, cn2an.an2cn(price / 100, "rmb"))
        worksheet.write(row, 1, count)
        row += 1
    workbook.close()
    file.seek(0)
    return send_file(file, attachment_filename="bills.xlsx", as_attachment=True)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=10002, debug=True)
