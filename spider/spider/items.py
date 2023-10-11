# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    author_name=scrapy.Field()
    author_url_token=scrapy.Field()
    author_type=scrapy.Field()
    author_follower_count=scrapy.Field()
    author_headline=scrapy.Field()
    answer_can_comment_reason=scrapy.Field()
    answer_can_comment_status=scrapy.Field()
    answer_comment_count=scrapy.Field()
    answer_comment_permission=scrapy.Field()
    answer_content=scrapy.Field()
    answer_voteup_count=scrapy.Field()
    
    
    
    
    
