# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import jieba

class FactorySpider(scrapy.Spider):
    name = 'factory'
    allowed_domains = ['y.zhaoshang800.com/']
    start_urls = ["https://weibo.com/perfectdiary?is_search=0&visible=0&is_hot=1&is_tag=0&profile_ftype=1&page=2#feedtop"]

    def parse(self, response):

        factories = response.css('.FL ul li a::attr(href)').extract()

        for f in factories:
            url = f
            item = None
            yield Request(url, meta={'url': url}, callback=self.parse_detail,dont_filter=True)

    def parse_detail(self,response):
        url = response.meta["url"]

        detail = response.css(".text::text").extract()
        item = {"title":None,"address":None,"industry":None,"product_name":None,"product_address":None,"total_area":None,"rental_area":None,"layer_height":None,"property":None,"power":None,"tranffic":None,"status":None,"status2":None,"mobile":None,"email":None,"user":None,"intro":None,}
        product_name = response.css(".cardCon span::text").extract()
        if len(product_name) == 3:

            item["product_name"] = product_name[0]
            item["title"] = product_name[1]
            item["industry"] = None
            item["address"] = product_name[2]
        elif len(product_name) == 4:

            item["product_name"] = product_name[0]
            item["title"] = product_name[1]
            item["industry"] = product_name[2]
            item["address"] = product_name[3]
        elif len(product_name) == 2:

            item["product_name"] = None
            item["title"] = product_name[0]
            item["industry"] = None
            item["address"] = product_name[1]

        yield Request(url+"main-jianjie.html#2", meta={'item': item,"url":url}, callback=self.parse_yuanqu, dont_filter=True)

    def parse_yuanqu(self,response):
        intro = response.css(".w1180 p::text").extract()
        item = response.meta["item"]
        url = response.meta["url"]

        # seg_list = jieba.cut(intro[4],cut_all=True)
        # for s in seg_list:
        #     print(s)
        item["intro"] = "".join(intro)
        yield Request(url + "main-lxfs.html#5", meta={'item': item, "url": url}, callback=self.parse_mobile,
                      dont_filter=True)


    def parse_mobile(self,response):
        item = response.meta["item"]
        url = response.meta["url"]
        product_address = response.css("#zbMapCurName::text").extract()
        info = response.css(".w1180 li::text").extract()
        item["mobile"] = info[-3]
        item["email"] = info[-2]
        item["user"] = info[-1]
        item["product_address"] = product_address[0] if len(product_address)>=1 else None
        yield item