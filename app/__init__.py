#teem_1
#p00
#10-28-25

from flask import Flask, render_template, request, session
import sqlite3


ACC_FILE = "users.db"

db = sqlite3.connect(ACC_FILE)
c = db.cursor()

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template('home.html')

@app.route("/login")
def login_page():
    return render_template('login.html')

@app.route("/create_acc")
def register_page():
    return render_template('create_acc.html')

app.debug = True
app.run()
'''
@app.route("edit_page")
def contribute(newWords, ):
    with


html: button submit runs contribute code,
'''
