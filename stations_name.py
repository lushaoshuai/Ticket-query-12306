import requests
import re 
from pprint import pprint
#re.findall findall函数返回的总是正则表达式在字符串中所有匹配结果的列表，
#此处主要讨论列表中“结果”的展现方式，即findall中返回列表中每个元素包含的信息。
#匹配中文字符正则表达式： [/u4e00-/u9fa5]
#4E00～9FFFh：中日韩认同表意文字区，总计收容20,902个中日韩汉字。
#pprint模块 提供了打印出任何Python数据结构类和方法，便于阅读

url='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018'
webdata=requests.get(url,verify=False).text
stations=dict(re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)',webdata))
if __name__=='__main__':
    pprint(stations, indent=4)
    print(stations['青岛']) 
    
