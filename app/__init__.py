#teem_1
#p00
#10-28-25

from flask import Flask, render_template, request, session, redirect
import sqlite3
from flask import request

ACC_FILE = "users.db"
STORY_FILE = "stories.db"

db = sqlite3.connect(ACC_FILE)
c = db.cursor()
sdb = sqlite3.connect(STORY_FILE)
sc = sdb.cursor()

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'asdhajskjbweifnoihgis'

#table for testing (remove after register works)
#c.execute("DROP TABLE if EXISTS users;")
c.execute("CREATE TABLE IF NOT EXISTS users(username text primary key, password text);")
#c.execute("INSERT INTO users VALUES('ricefarmer', 'riceplant'),('ricefarmer2', 'ricerice'),('ricefarmer3','ecir');")
db.commit()
db.close()
#table for testing (remove after stories.db works)
#sc.execute("DROP TABLE if EXISTS stories;")
sc.execute("CREATE TABLE IF NOT EXISTS stories(title text primary key, genre text, length int, content text);")
#sc.execute("INSERT INTO stories VALUES('gameTitle', 'Horror', 32, 'This is the craziest story ever.');")
sdb.commit()
sdb.close()

#trying to make proxy page that does the logic, i was running into an issue
#with trying to make it only redirect you after you click the button
#not sure now

@app.route("/redirect_login", methods=['GET', 'POST'])
def redirect_login():
    #session.pop('username',None) #to reset session since we dont have logout yet
    if 'username' in session:
        return redirect('/home')
    testUser = request.form.get('username')
    testPass = request.form.get('password')

    db = sqlite3.connect(ACC_FILE)
    c = db.cursor()
    check = c.execute(f"SELECT COUNT(*) FROM users WHERE username = '{testUser}' AND password = '{testPass}';")
    result = check.fetchone()[0]
    if result == 0:
        return render_template('login.html')
    else:
        session['username'] = request.form.get('username')
        return redirect('/home')
    db.commit()
    db.close()
    return render_template('login.html')

@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.pop('username',None)
    return redirect('/')

@app.route("/", methods=['GET', 'POST'])
def login_page():
    if 'username' in session:
        return redirect('/home')
    #session.pop('username',None) #to reset session since we dont have logout yet
    return render_template('login.html')

@app.route("/home", methods=['GET', 'POST'])
def home_page():
    if not session.get('username'):
        return redirect('/')
    print("username: " + session['username'])
    return render_template('home.html')

@app.route('/redirect_create', methods=['POST', 'GET'])
def redirect_create():
    if 'username' in session:
        return redirect('/home')
    testUser = request.form.get('username')
    testPass = request.form.get('password')
    print(testPass)
    if not testUser or not testPass:
        return redirect('/create_acc')
    db = sqlite3.connect(ACC_FILE)
    c = db.cursor()
    check = c.execute(f"SELECT COUNT(*) FROM users WHERE username = '{testUser}';")
    result = check.fetchone()[0]
    if result == 0:
        c.execute(f"INSERT INTO users VALUES ('{testUser}', '{testPass}');")
        db.commit()
        db.close()
        session['username'] = testUser
        return redirect('/home')
    else:
        db.close()
        return redirect('/create_acc')

@app.route("/create_acc")
def register_page():
    return render_template('create_acc.html')

@app.route("/browse_page")
def browse_page():
    return render_template('browse.html')


app.debug = True
app.run()

'''
@app.route("/edit_page")
def contribute(newWords, ):
    with


html: button submit runs contribute code,
'''
