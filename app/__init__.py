#teem1
#p00
#10-28-25

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)    #create Flask object

@app.route("/")
def main_page():
    return "this is the app!!"
@app.route("/register", methods = ['GET', 'POST'])
def register(): 
	message = ' '
	if request.method == 'POST' and 'name' in request.form and 'password'in request.form: 
		username = request.form['name']
		password = request.form['password'] 
		#--stopped 
app.debug = True
app.run()
