import pymysql.cursors
from datetime import datetime
import json

mydb = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='world',
                            )

try:
    # 커서 생성
    with mydb.cursor() as cursor:
        # 테이블 생성 쿼리
        create_table_query = """
        CREATE TABLE fandata (
            id INT(11) NOT NULL AUTO_INCREMENT,
            srialNum VARCHAR(100) NOT NULL,
            daydate DATETIME NOT NULL,
            skills JSON,
            PRIMARY KEY (id)
        )
        """

        # 테이블 생성
        # cursor.execute(create_table_query)

        # 배열 데이터 생성 (예시로 1000개의 데이터 생성)
        skills_data = []
        for i in range(1000):
            skills_data.append(f"{1000-i}")

        # 배열 데이터를 JSON 형식으로 변환
        skills_json = json.dumps(skills_data)

        # 데이터 삽입 쿼리
        insert_data_query = """
        INSERT INTO fandata (srialNum, daydate, skills)
        VALUES (%s, %s, %s)
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 데이터 삽입
        cursor.execute(insert_data_query, ('ABC000', current_time, skills_json))

    # 변경사항을 커밋
    mydb.commit()

    print("데이터가 성공적으로 삽입되었습니다.")

finally:
    # 연결 종료
    mydb.close()