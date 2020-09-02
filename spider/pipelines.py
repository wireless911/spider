# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


import codecs
import json

from openpyxl import Workbook


class ExcelPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['公司名称', '园区名称/产业名称', '园区地址', '总建面', '出租面积', '主体层高', '产权性质', '厂房配电', '交通优势',"园区现状","招商业态","电话","邮箱","联系人","产业行业","项目概要"])

    def process_item(self, item, spider):
        line = [item['product_name'], item['title'], item['address'], item['total_area'], item['rental_area'],
                item['layer_height'], item['property'], item['power'], item['tranffic'], item['status'],item['status2'],item['mobile'],item['email'],item['user'],item["industry"],item['intro']]
        self.ws.append(line)
        self.wb.save('./excel/海口.xlsx')
        return item







class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):  # 初始化，打开文件
        self.file = codecs.open('article.json', 'w', encoding="utf-8")
        # 这里用codecs库来打开文件，目的是编码不会出错

    def process_item(self, item, spider):  # 写入文件
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):  # 关闭文件
        self.file.close()

from scrapy.exporters import CsvItemExporter

class EnrolldataPipeline(object):
    def open_spider(self, spider):
        self.file = open("article.csv", "wb")
        self.exporter = CsvItemExporter(self.file,
        fields_to_export=["title", "address", "industry","product_name","product_address","total_area","rental_area","layer_height","property","power","tranffic","status","mobile","intro"])
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
