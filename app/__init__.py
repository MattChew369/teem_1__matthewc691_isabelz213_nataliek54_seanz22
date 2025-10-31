#teem_1
#p00
#10-28-25

from flask import Flask, render_template, request, session, redirect
import sqlite3
from flask import request

ACC_FILE = "users.db"

db = sqlite3.connect(ACC_FILE)
c = db.cursor()

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'asdhajskjbweifnoihgis'

@app.route("/", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect('/home')
    elif session['username']:
        return redirect('/home')
    return render_template('login.html')

@app.route("/home")
def home_page():
    if not session.get('username'):
        return redirect('/login.html')
    return render_template('home.html')

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
