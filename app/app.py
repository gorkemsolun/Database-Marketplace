
import re  
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__) 

app.secret_key = 'abcdefgh'
  
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cs353hw4db'
  
mysql = MySQL(app)  

@app.route('/')

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE name = % s AND cid = % s', (username, password, ))
        user = cursor.fetchone()
        if user:              
            session['loggedin'] = True
            session['userid'] = user['cid']
            session['username'] = user['name']
            message = 'Logged in successfully!'
            return redirect(url_for('main_page'))
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message = message)

@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE name = % s', (username, ))
        account = cursor.fetchone()
        if account:
            message = 'Choose a different username!'
  
        elif not username or not password:
            message = 'Please fill out the form!'

        else:
            cursor.execute('INSERT INTO customer (cid, name) VALUES (% s, % s)', (password, username))
            mysql.connection.commit()
            message = 'User successfully created!'

    elif request.method == 'POST':

        message = 'Please fill all the fields!'
    return render_template('register.html', message = message)

@app.route('/main')
def main_page():
  return "Main page"

@app.route('/money_transfer', methods=['GET', 'POST'])
def money_transfer():
   return "Money transfer"

@app.route('/close_account/<aid>', methods=['GET', 'POST'])
def close_account(aid):
   return "Close account"

@app.route('/account_summary')
def account_summary():
    return "Account summary"

@app.route('/logout')
def logout():
  return "Logout"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
