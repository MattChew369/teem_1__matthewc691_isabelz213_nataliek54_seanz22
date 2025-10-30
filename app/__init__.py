#teem1
#p00
#10-28-25

from flask import Flask, render_template, request, session
import sqlite3

app = Flask(__name__)    #create Flask object

@app.route("/")
def main_page():
    return render_template('home.html')

@app.route("/login")
def login_page():
    return render_template('login.html')

app.debug = True
app.run()
