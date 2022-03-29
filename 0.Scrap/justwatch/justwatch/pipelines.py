# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import MySQLdb


class JustwatchPipeline:
    def process_item(self, item, spider):
        return item

from scrapy.exporters import CsvItemExporter, XmlItemExporter, JsonItemExporter
class CsvPipeline(object):
    def __init__(self):
        self.file = open("assets/movies.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()
 
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
 
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

# 0323 추가 

class MySQLPipeline(object):
    """
    Item을 MySQL에 저장하는 Pipeline
    """
    
    def open_spider(self, spider):
        """
        Spider를 시작할 때 MySQL 서버에 접속합니다.
        items 테이블이 존재하지 않으면 생성합니다.
        """
        # settings.py에서 설정을 읽어 들입니다.
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', '3.35.111.73'),
            'db': settings.get('MYSQL_DATABASE', '99'),
            'user': settings.get('MYSQL_USER', 'carbon'),
            'passwd': settings.get('MYSQL_PASSWORD', '1111'),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }

        # # settings.py에서 설정을 읽어 들입니다.
        # settings = spider.settings
        # params = {
        #     'host': settings.get('MYSQL_HOST', 'localhost'),
        #     'db': settings.get('MYSQL_DATABASE', 'scraping'),
        #     'user': settings.get('MYSQL_USER', ''),
        #     'passwd': settings.get('MYSQL_PASSWORD', ''),
        #     'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        # }

        # MySQL 서버에 접속합니다.
        self.conn = MySQLdb.connect(**params) 
        # 커서를 추출합니다.
        self.c = self.conn.cursor() 
        # items 테이블이 존재하지 않으면 생성합니다.
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER NOT NULL AUTO_INCREMENT,
                title CHAR(200) NOT NULL,
                PRIMARY KEY (id)
            )
        ''')
        # 변경을 커밋합니다.
        self.conn.commit()
    
    def close_spider(self, spider):
        """
        Spider가 종료될 때 MySQL 서버와의 접속을 끊습니다.
        """
        self.conn.close()
    def process_item(self, item, spider):
        """
        Item을 items 테이블에 삽입합니다.
        """
        self.c.execute('INSERT INTO items (title) VALUES (%(title)s)', dict(item))
        self.conn.commit()
        return item