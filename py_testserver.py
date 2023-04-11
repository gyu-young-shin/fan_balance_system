import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='world',
                            )

try:
    cursor = connection.cursor()
    sql = "select * from users"
    cursor.execute(sql)

    #print(cursor.fetchall())

    rows = cursor.fetchall()
    for i in rows :
     print(i)
finally:
    cursor.close()
    connection.close()