import os

from xlutils.copy import copy
from os import listdir
import xlrd
import requests
import json
# 设置路径
path = './test.xlsx'
# url = "http://api.map.baidu.com/geocoding/v3/?address={address}&output=json&ak=grSKFtZfmK6LUwptsC6aGuv9WeeVZgfG"
url = "http://api.map.baidu.com/geocoding/v3/?address={address}&output=json&ak=fZIHG6u9iL8YAyGiLv2NjxrCndGKlh9U"

class Excel(object):
    def __init__(self,input_path,out_put_path):
        self.path_list = listdir(input_path)
        for path in self.path_list:
            if os.path.exists((out_put_path+path)[:-1]):
                continue
            if self.open_copy_excel(input_path+path):
                if self.write_data(out_put_path+path):
                    print("over")
                else:
                    break

    def open_copy_excel(self,path):
        # 打开execl
        workbook = xlrd.open_workbook(path) #formatting_info = True
        self.new_workbook = copy(workbook)

        self.write_s = self.new_workbook.get_sheet(0)
        # 输出Excel文件中所有sheet的名字
        print(workbook.sheet_names())
        # 根据sheet索引或者名称获取sheet内容
        Data_sheet = workbook.sheets()[0]  # 通过索引获取
        colNum = Data_sheet.ncols  # sheet列数
        self.rowNum = Data_sheet.nrows  # sheet行数
        self.cols = Data_sheet.col_values(2)  # 获取地址列内容
        return True

    def write_data(self,path):
        self.write_s.write(0,16,"经度")
        self.write_s.write(0,17,"纬度")
        for rowCount in range(1, self.rowNum):
            # get 请求
            response = requests.get(url.format(address=self.cols[rowCount]))
            # 字符串转json
            json_obj = json.loads(response.content)
            if json_obj.get("status")==302:
                print("break response 302  配额超过")
                return False
            if  json_obj.get("result"):
                if  json_obj.get("result").get("location"):
                    jingdo = json_obj.get("result").get("location").get("lng")
                    weidu = json_obj.get("result").get("location").get("lat")
                    # result = LatLng_Dec2Rad(jingdo) + "/" + LatLng_Dec2Rad(weidu)
                    self.write_s.write(rowCount,16,jingdo)
                    self.write_s.write(rowCount,17,weidu)
        self.new_workbook.save(path[:-1])
        return True

    @staticmethod
    def LatLng_Dec2Rad(decNum):
        NumIntegral = int(decNum)  # 整数部分
        NumDecimal = decNum - NumIntegral  # 小数部分

        tmp = NumDecimal * 3600
        degree = NumIntegral  # 度
        minute = int(tmp // 60)  # 分
        second = tmp - minute * 60  # 秒 tmp%3600
        return str(degree) + "," + str(minute) + "," + str(second)



if __name__ == '__main__':
    ex = Excel("./excel/","./new_excel/")