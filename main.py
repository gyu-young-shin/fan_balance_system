from flask import Flask, render_template, request, redirect, url_for, session
import pymysql.cursors

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
        return 'Logged in as ' + session['username'] + '<br>' + \
            "<b><a href = '/logout'>click here to log out</a></b>"
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
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True , host='192.168.0.2', port=8000)