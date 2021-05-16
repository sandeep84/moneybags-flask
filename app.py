from flask import Flask
from flask import render_template
from datetime import datetime
import re

import accountManager

app = Flask(__name__)

@app.route("/")
@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/accounts")
def accountsView():
    accounts = accountManager.getAccounts()
    return render_template(
        "accounts.html",
        accounts=accounts
    )

@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js'), 200, {'Content-Type': 'text/javascript'}
