# Description 

"""
파일패스를 입력받아. DB에 저장합니다. 
csv를 이용하며. AWS EC2 MySQL DB와 연동됩니다.
"""

from gc import callbacks
import pymysql
import pandas as pd
import numpy as np


path = r"C:\Users\jlune\carbon\project_JI\02.DB\synopsis_filter.csv"
data = pd.read_csv(path, keep_default_na=False)
"""패스를 인자로 받아 df에 저장. MySQL 에 NaN 값 들어갈시 에러가 나기에
    keep_default_na = False 옵션으로 None 타입으로 들어가도록 한다"""

# DB에 connect
conn = pymysql.connect(host='3.35.111.73',
                       port=3306,
                       user='carbon',
                       password='1111',
                       db='testdb',
                       charset='utf8mb4')

# 커서 생성
cursor = conn.cursor()

""" 쿼리문 작성 및 실행 """

# testdb 에 Base 테이블 생성
sql1 = '''CREATE TABLE testdb.test_1
        (       
                MV_NO int(13) NOT NULL PRIMARY KEY,
                TITLE varchar(4000),
                OPEN_DATE varchar(1000),
                JUST_RATING varchar(1000),
                IMDB_RATING varchar(1000),
                RUNTIME varchar(500),
                SYNOPSIS varchar(4000),
                DIRECTOR varchar(1000),
                ACTORS varchar(4000),
                GENRE varchar(4000),
                POSTER_LINK varchar(1000),
                NETFLIX int,
                DISNEY int,
                WAVVE int,
                WATCHA int
        ) '''
        
cursor.execute(sql1)

# user table 에 값 insert
sql2 = '''INSERT INTO test_1 (MV_NO, TITLE, OPEN_DATE, JUST_RATING, IMDB_RATING, 
                RUNTIME, SYNOPSIS, DIRECTOR, ACTORS, GENRE, POSTER_LINK, NETFLIX, DISNEY, WAVVE, WATCHA) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                
for idx in range(len(data)):
    cursor.execute(sql2, tuple(data.values[idx]))  # data.values[idx] 는 배열이기에 튜플타입을 활용한다. 

conn.commit()
conn.close()





