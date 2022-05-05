# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MpeiscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    surname = scrapy.Field()
    patronymic = scrapy.Field()
    position = scrapy.Field()
    url = scrapy.Field()
    email = scrapy.Field()
    science_degree = scrapy.Field()
    scientific_title = scrapy.Field()
    pass
