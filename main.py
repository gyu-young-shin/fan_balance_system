from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO
import pymysql.cursors
import datetime
import random
import json
#!-------------------------------------------------------------------------
#!-------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "your_secret_key"


mydb = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='world',
                            )
#!-------------------------------------------------------------------------
#!-------------------------------------------------------------------------

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
#!-------------------------------------------------------------------------
#!-------------------------------------------------------------------------

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

#!-------------------------------------------------------------------------
#!-------------------------------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

#!-------------------------------------------------------------------------
#!-------------------------------------------------------------------------
@app.route('/update_data')
def update_data():
    currnettime = datetime.datetime.now()
    print(currnettime)
    
    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
    # values = [10, 20, 30, 40, 50, 60, 70]
    values = [random.randint(1, 45) for _ in range(7)]
    print(values)
    # return jsonify(labels=labels, values=values ,currnettime=currnettime)
    
    return jsonify(labels=labels, values=values ,currnettime=currnettime)

#!-------------------------------------------------------------------------
#!------------------------------------------------------------------------- 
 
@app.route('/search', methods=['GET'])
def search():
    # Form 데이터에서 선택한 날짜 가져오기
    cursor = mydb.cursor()

    # 특정 날짜에 해당하는 레코드 검색 쿼리
    sql = "SELECT * FROM fandata WHERE DATE(daydate) BETWEEN %s AND %s"
    search_date = request.args.get('searchDate')
    
    start_date = search_date[0:10]
    end_date =search_date[10:]
    
    if search_date is None:
    # 데이터가 없는 경우 기본 값을 설정하거나 에러 처리를 수행할 수 있습니다.
    # 기본 값 설정 예시:
         start_date = '2023-05-12'
         end_date = '2023-05-12'
         
    # 쿼리 실행
    cursor.execute(sql, (start_date, end_date))
    
    # 검색 결과 가져오기
    results = cursor.fetchall()
    
    # print(results)
    # 결과 출력
    # for row in results:
    #     print(row)
    
    serialNum = []
    daydate=[]
    for row in results:
        id = row[0]
        serialNum.append(row[1])
        daydate.append(row[2])
        skills_json = row[3]

    # Process the data as needed
    # Example: Print the values of each column
        # print(f"ID: {id}")
        # print(f"Serial Number: {srialNum}")
        # print(f"Day Date: {daydate}")
        # print(f"Skills JSON: {skills_json}")
    print(serialNum)

    # mydb.close()
    
    return jsonify(serialNum=serialNum, daydate=daydate)
    # return render_template('result.html', data=result)


@app.route('/tabledb', methods=['GET'])
def tabledb():
    dbDate = request.args.get('dbDate')
    print(dbDate)
    cursor = mydb.cursor()
    sql = "SELECT * FROM fandata WHERE srialNum = %s"
    cursor.execute(sql, (dbDate,))
    results = cursor.fetchall()
    
    skills_data = []
    
    for row in results:
        skills_json = row[3]
        skills = json.loads(skills_json)
        skills_data.extend(skills)
        
    # print(skills_data)
    return jsonify(skills_data=skills_data)

#!-------------------------------------------------------------------------
#!-------------------------------------------------------------------------    
if __name__ == '__main__':
    # app.run(debug=True , host='192.168.0.2', port=8000)
    # app.run(debug=True , host='127.0.0.1', port=8000)

     app.run(debug=True , host='127.0.0.1', port=8000)
    # socketio.run(app, debug=True,host='127.0.0.1', port=8000)

#!-------------------------------------------------------------------------
#!-------------------------------------------------------------------------    