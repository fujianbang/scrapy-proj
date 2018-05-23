# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsItem(scrapy.Item):
    # 职位名称
    job_name = scrapy.Field()
    # 职位描述
    job_summary = scrapy.Field()
    # 学历需求
    job_require_degree = scrapy.Field()
    # 经验需求
    job_require_experience = scrapy.Field()
    # 招聘人数
    job_require_number = scrapy.Field()
    # 公司名称
    company_name = scrapy.Field()
    # 地区
    regin = scrapy.Field()
    # 薪资
    salary = scrapy.Field()
    # 联系方式
    contact = scrapy.Field()
    # 发布时间
    publish_time = scrapy.Field()
    # 原始URL
    origin_url = scrapy.Field()
