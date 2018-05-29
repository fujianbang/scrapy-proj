# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from urllib.parse import quote

from jobs.items import JobsItem

class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']

    current_page = 1

    def start_requests(self):
        # 软件工程师
        p_type = "软件工程师"
        # Python Java C Php Go js
        start_url = "https://search.51job.com/list/000000,000000,0000,32,9,99,js,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=4&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        # 拼接起始URL
        url = start_url.format(p_type, 1)
        yield Request(url, callback=self.parse_urls)
        
        '''
        url = "https://jobs.51job.com/shanghai-mhq/101892898.html?t=2&s=01"
        url = "http://jobs.51job.com/shanghai-mhq/85502775.html?s=01&t=0"
        yield Request(url, callback=self.parse)
        '''

    def parse_urls(self, response):
        """
        解析目录的URL
        """
        print("第{}页".format(self.current_page))
        urls = response.xpath("//*[@id='resultList']/div[@class='el']/p/span/a/@href").extract()
        for url in urls:
            print("Target Url:\t" + url)
            yield Request(url, callback=self.parse)

        # 解析下一页url
        next_page = response.xpath("//div[@class='dw_page']/div[@class='p_box']/div[@class='p_wp']/div[@class='p_in']/ul/li[@class='bk']/a/@href").extract()
        if len(next_page) == 0:
            # 下一页为空，则爬取到最后一页
            return
        next_page_url = next_page[len(next_page)-1]
        self.current_page += 1
        yield Request(next_page_url, callback=self.parse_urls)

    def parse(self, response):
        """
        内容网址解析
        """
        item = JobsItem()
        item['job_name'] = response.xpath("//div[@class='cn']/h1/text()").extract()[0]
        item['job_summary'] = response.xpath("//div[contains(@class, 'bmsg') and contains(@class, 'job_msg') and contains(@class, 'inbox')]").re("<div class=\"bmsg job_msg inbox\">[\s\S]*<div class=\"mt10\">")[0][32:-18]
        item['contact'] = response.xpath("//div[contains(@class, 'bmsg') and contains(@class, 'inbox')]/p[@class='fp']/text()").extract()[0]
        # require element 
        require_elements = response.xpath("//div[contains(@class, 'jtag') and contains(@class, 'inbox')]/div[@class='t1']/span[@class='sp4']")
        try:
            item['job_require_degree'] = require_elements.xpath("em[@class='i2']/ancestor::span[@class='sp4']/text()").extract()[0]
            item['job_require_experience'] = require_elements.xpath("em[@class='i1']/ancestor::span[@class='sp4']/text()").extract()[0]
            item['job_require_number'] = require_elements.xpath("em[@class='i3']/ancestor::span[@class='sp4']/text()").extract()[0]
            item['publish_time'] = require_elements.xpath("em[@class='i4']/ancestor::span[@class='sp4']/text()").extract()[0]
        except:
            pass
        # company regin salary
        item['company_name'] = response.xpath("//div[@class='cn']/p[@class='cname']/a/text()").extract()[0]
        item['regin'] = response.xpath("//div[@class='cn']/span[@class='lname']/text()").extract()[0]
        item['salary'] = response.xpath("//div[@class='cn']/strong/text()").extract()[0]
        item['origin_url'] = response.url
        yield item
