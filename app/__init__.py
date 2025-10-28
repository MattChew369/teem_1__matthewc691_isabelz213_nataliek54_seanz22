#teem1
#p00
#10-28-25

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)    #create Flask object

@app.route("/")
def main_page():
    return "this is the app!!"

app.debug = True
app.run()
