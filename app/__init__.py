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
sc.execute("DROP TABLE if EXISTS stories;")
sc.execute("CREATE TABLE IF NOT EXISTS stories(title text primary key, genre text, length int, content text, username text, link text);")
#sc.execute("INSERT INTO stories VALUES('gameTitle', 'Horror', 32, 'This is the craziest story ever.');")
sc.execute("INSERT INTO stories VALUES('Sold to One Direction', 'Horror', 4, 'NOO!', 'Test', 'sold_to_one_direction');")
sc.execute("INSERT INTO stories VALUES('Lorem Ipsum', 'Adventure', 80, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'Test', 'lorem_ipsum');")
sdb.commit()
sdb.close()

#trying to make proxy page that does the logic, i was running into an issue
#with trying to make it only redirect you after you click the button
#not sure now

def title_to_link(title):
    title = title.split(' ')
    link = ''
    for i in range(len(title) - 1):
        link += title[i].lower() + '_'
    link += title[len(title) - 1]
    return link

def link_to_title(link):
    link = link.split('_')
    title = ''
    for i in range(len(link) - 1):
        title += link[i].title() + ' '
    title += link[len(link) - 1]
    return title

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
    username = session['username']
    db = sqlite3.connect(STORY_FILE)
    c = db.cursor()
    c.execute ("SELECT title FROM stories WHERE username = ?", (username,)) #for listing story titles later & only lists the stories created by logged-in
    stories = c.fetchall()
    db.close()
    return render_template('home.html', user = username, stories = stories) #renders page w/ data

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
    db = sqlite3.connect(STORY_FILE)
    c = db.cursor()
    check_long = c.execute(f"SELECT title FROM stories WHERE title IN (SELECT title FROM stories) ORDER BY title DESC LIMIT 5;")
    results = check_long.fetchall()
    results = [x[0] for x in results]
    check_link = c.execute(f"SELECT link FROM stories WHERE title IN (SELECT title FROM stories) ORDER BY title DESC LIMIT 5;")
    links = check_link.fetchall()
    links = [x[0] for x in links]
    return render_template('browse.html', stories=results)

@app.route('/story/<string:link>')
def story(link):
    db = sqlite3.connect(STORY_FILE)
    c = db.cursor()
    check = c.execute(f"SELECT * FROM stories WHERE link = '" + link + "';")
    title = check.fetchall()
    title = list(title[0])
    print(title)
    if (len(title) == 0):
        return ("Error: no story exists here.")
    elif (len(title) > 6):
        return ("Story naming error")
    else:
        return render_template('story.html', title=link_to_title(link), starter=title[4], genre=title[1], content=title[3])

@app.route('/redirect_add_story', methods= ['POST'])
def redirect_add_story():
    if 'username' not in session:
        return redirect ('/')
    title = request.form.get('title')
    genre = request.form.get('genre')
    content = request.form.get('content')
    username = session['username']
    if not title or not content:
        return redirect('/add_story')
    db = sqlite3.connect(STORY_FILE)
    c = db.cursor()
    c.execute(f"INSERT INTO stories VALUES ('{title}', '{genre}', '{len(content)}', '{content}', '{username}', '{title_to_link(title)}');")
    db.commit()
    db.close()
    return redirect('/home')


@app.route('/add_story')
def add_story():
    return render_template('add_story.html')


app.debug = True
app.run()



'''
@app.route("/edit_page")
def contribute(newWords, ):
    with


html: button submit runs contribute code,
'''
