from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO
import pymysql.cursors
import datetime
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"


mydb = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='world',
                            )


@app.route('/')
def index():
    if 'username' in session:
        # return 'Logged in as ' + session['username'] + '<br>' + \
        #     "<b><a href = '/logout'>click here to log out</a></b>"
        # scheduler = BackgroundScheduler()
        # scheduler.add_job(func=update_database, trigger='interval', seconds=5)
        # scheduler.start()
        
        return render_template('main.html' )
    return render_template('login1.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            return render_template('login1.html', error='Invalid username or password')
    return render_template('login1.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/update_data')
def update_data():
    currnettime = datetime.datetime.now()
    print(currnettime)
    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
    # values = [10, 20, 30, 40, 50, 60, 70]
    values = [random.randint(1, 45) for _ in range(7)]
    print(values)
    return jsonify(labels=labels, values=values ,currnettime=currnettime)
    

if __name__ == '__main__':
    # app.run(debug=True , host='192.168.0.2', port=8000)
    # app.run(debug=True , host='127.0.0.1', port=8000)

     app.run(debug=True , host='127.0.0.1', port=8000)
    # socketio.run(app, debug=True,host='127.0.0.1', port=8000)
  