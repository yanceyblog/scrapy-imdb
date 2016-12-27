# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class ImdbItem(Item):
    # define the fields for your item here like:
    video_title = Field()
    video_rating = Field()
    video_name = Field()
    video_alias = Field()
    video_director = Field()
    video_actor = Field()
    video_length = Field()
    video_language = Field()
    video_year = Field()
    video_type = Field()
    video_color = Field()
    video_area = Field()
    video_voice = Field()
    video_summary = Field()
    video_url = Field()
