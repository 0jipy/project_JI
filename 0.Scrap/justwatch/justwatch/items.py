# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JustwatchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title_kor = scrapy.Field()
    opening_date = scrapy.Field()
    just_rating = scrapy.Field()
    imdb_rating = scrapy.Field()
    runtime = scrapy.Field()
    synopsis = scrapy.Field()
    director = scrapy.Field()
    synopsis = scrapy.Field()
    actors = scrapy.Field()
    genre = scrapy.Field()

    # 0317 buid
