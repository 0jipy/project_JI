# Description 

"""
파일패스를 입력받아. DB에 저장합니다. 
csv를 이용하며. AWS EC2 MySQL DB와 연동됩니다.
"""

from gc import callbacks
import pymysql
import pandas as pd


def Input_path(self, path, Keep_default_na=False):
    """패스를 인자로 받아 df에 저장. MySQL 에 NaN 값 들어갈시 에러가 나기에
    keep_default_na = False 옵션으로 None 타입으로 들어가도록 한다"""
    data = pd.read_csv(r+f'{path}', keep_default_na=False)
    # print(path)
    callbacks(self,In_mysql)

def In_mysql(self):
    print("끝")






