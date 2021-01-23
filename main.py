from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NoT$ecR3tK3y1679'

db = sqlite3.connect('app.db')
print('Opened database successfully')

db.execute('CREATE TABLE IF NOT EXISTS accounts (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL);')
db.execute('CREATE TABLE IF NOT EXISTS tasks (task_id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL, username TEXT NOT NULL);')
print('account table created')
print('tasks table created')
db.close()

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pw']
        with sqlite3.connect('app.db') as db:
            cur = db.cursor()
            query2 = 'SELECT * FROM accounts WHERE username = ? AND password = ?;'
            cur.execute(query2, (username, password, ))
            account = cur.fetchone()
            if account:
                session['loggedin'] = True
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                msg = 'Incorrect username or password!'
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register/', methods=['POST', 'GET'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pw']
        email = request.form['email']
        with sqlite3.connect('app.db') as db:
            cur = db.cursor()
            query = 'SELECT * FROM accounts WHERE username = ?;'
            cur.execute(query, (username, ))
            account = cur.fetchone()
            if account:
                msg = 'Account already exists!'
            elif not username or not email or not password:
                msg = 'Please make sure the form is filled out!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invaid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            else:
                query1 = "INSERT INTO accounts VALUES(NULL, ?, ?, ?);"
                cur.execute(query1, (username, email, password, ))
                db.commit()
                return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg =msg)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'GET':
        if 'loggedin' in session:
            username = session['username']
            with sqlite3.connect('app.db') as db:
                    cur = db.cursor()
                    query = 'SELECT task_id, task FROM tasks WHERE username = ?;'
                    cur.execute(query, (username, ))
                    tasks = cur.fetchall()
            return render_template('dashboard.html', uname=session['username'], tasks=tasks) 

@app.route('/add', methods=['POST', 'GET'])
def add_task():
    if request.method == 'POST':
        if request.form['add_task']:
            a_task = request.form.get('add_task')
            username = session['username']
            with sqlite3.connect('app.db') as db:
                cur = db.cursor()
                query = 'INSERT INTO tasks (username, task) VALUES (?,?);'
                cur.execute(query, (username, a_task, ))
                db.commit()
        return render_template('add.html')
    else:
        return redirect(url_for('dashboard'))
        
@app.route('/delete', methods=['POST', 'GET'])
def del_task():
    if request.method == 'POST':
        if request.form['del_task']:
            d_task = request.form.get('del_task')
            with sqlite3.connect('app.db') as db:
                cur = db.cursor()
                query1 = 'DELETE FROM tasks WHERE task_id = ?;'
                cur.execute(query1, (d_task, ))
        return render_template('delete.html')
    else:
        return redirect(url_for('dashboard'))
            

if (__name__ == '__main__'):
    app.run(debug=True, host='0.0.0.0')           