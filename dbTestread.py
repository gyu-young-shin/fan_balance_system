import pymysql

mydb = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='world',
                            )

try:
    with mydb.cursor() as cursor:
        # 특정 날짜에 해당하는 레코드 검색 쿼리
        sql = "SELECT * FROM fandata WHERE DATE(daydate) = %s"
        
        # 원하는 날짜
        date = '2023-05-12'
        
        # 쿼리 실행
        cursor.execute(sql, (date,))
        
        # 검색 결과 가져오기
        results = cursor.fetchall()
        
        print(results)
        # 결과 출력
        # for row in results:
        #     print(row)
finally:
    # 연결 닫기
    mydb.close()