#coding: utf-8
'''火车票查询工具
Usage:
    12306 [-gdtkz] <from> <to> <data>   

Options:
    -h,--help  显示帮助菜单
    -g         高铁 
    -d         动车
    -t         特快
    -k         快速
    -z         直达  
Example:
    12306 北京 上海 2015-11-14
    12306 -gd 南京 哈尔滨 2016-04-5
    
'''
from docopt import docopt
from stations_name import stations
import requests
from prettytable import PrettyTable
from colorama import init,Fore

stations_reserve={v:k for k,v in stations.items()}
init()

class Analyse():
    header='车次 车站 时间 历时 商务座 一等座 二等座 高级软卧 软卧 动卧 硬卧 软座 硬座 无座 其他'.split()
    def __init__(self,available_trains,options):
        self.available_trains=available_trains
        self.options=options

        
    
    def _duration(self,raw_train):
        duration=raw_train.get('lishi').replace(':','小时')+'分'
        if duration.startswith('00'):
            return duration[4:]
        elif duration.startswith('0'):
            return duration[1:]
        else:
            return duration
    
    @property
    def trains(self):
        for raw_train in self.available_trains:
            train_no=raw_train['checi']
            initial=train_no[0].lower()
            if not self.options or initial in self.options:
                train=[train_no,'\n'.join([Fore.GREEN + stations_reserve.get(raw_train['from_station']) + Fore.RESET,
                                           Fore.RED + stations_reserve.get(raw_train['to_station']) + Fore.RESET]),
                                 '\n'.join([Fore.GREEN + raw_train['start_time'] + Fore.RESET,
                                           Fore.RED + raw_train['arrive_time'] + Fore.RESET]),
                       self._duration(raw_train), 
                       raw_train['shangwu'],
                       raw_train['yideng'],
                       raw_train['erdeng'],
                       raw_train['gaojiruanwo'],
                       raw_train['ruanwo'],
                       raw_train['dongwo'],
                       raw_train['yingwo'],
                       raw_train['ruanzuo'],
                       raw_train['yingzuo'],
                       raw_train['wuzuo'],
                       raw_train['qita'],

                       ]
                yield train
                
    def pretty_print(self):
        pt=PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)
       
def inquiry():
    results=docopt(__doc__)
    print(results)

    from_station=stations.get(results['<from>'])
    to_station=stations.get(results['<to>'])
    data=results['<data>']
    #构建URL

    url='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(data,from_station,to_station)

    #获取数据

    r=requests.get(url,verify=False)
    available_trains=[]
    sourcedata=r.json()['data']['result']   
    for i in range(0,len(sourcedata)):
        m=sourcedata[i].split('|')
        inf={
                    'checi':m[3],
                    'from_station':m[4],
                    'to_station':m[7],
                    'start_time':m[8],
                    'arrive_time':m[9],
                    'lishi':m[10],
                    'data':m[13],
                    'shangwu':m[-4] or '--',
                    'yideng':m[-5] or '--',
                    'erdeng':m[-6] or '--',
                    'gaojiruanwo':m[-7] or '--',
                    'ruanwo':m[-8] or '--',
                    'dongwo':m[-9] or '--',
                    'yingwo':m[-10] or '--',
                    'ruanzuo':m[-11] or '--',
                    'yingzuo':m[-12] or '--',
                    'wuzuo':m[-13] or '--',
                    'qita':m[-14] or '--'          
                    }
        available_trains.append(inf)
    #print(available_trains)
    
    '''
    results.items()将字典key value 在字典中存放为一个新的列表

    '''
    options=''.join([key for key,value in results.items() if value is True])
    
    Analyse(available_trains,options).pretty_print()
if __name__=='__main__':
    inquiry()
    

