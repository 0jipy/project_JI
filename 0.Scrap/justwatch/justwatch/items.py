import scrapy

class JustwatchItem(scrapy.Item):
    a_title_kor = scrapy.Field()
    b_opening_date = scrapy.Field()
    c_just_rating = scrapy.Field()
    imdb_rating = scrapy.Field()
    runtime = scrapy.Field()
    synopsis = scrapy.Field()
    director = scrapy.Field()
    actors = scrapy.Field()
    genre = scrapy.Field()      
