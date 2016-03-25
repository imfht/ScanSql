import re
from bs4 import BeautifulSoup
import requests
from urllib import parse
import urllib.parse as urlparse
import queue
webSiteSet = set()
fuck_set = set()
class WebSite():
    #一个WebSite应该有的属性 
    def __init__(self,name,url):
        self.name = name
        self.url = url
        self.dic = {} #key->路径 value->参数
    def put_link(self,url):
        self.set.add(url)
class BigFuck():
    def __init__(self,url):
        self.url = url
        self.friend_url = []
        self.payload_url = set()
        self.attach_url = queue.Queue()
        self.testSet = set()
    def get_things(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text,'lxml')
        #print(req.text)
        pattern = re.compile('href="(.*?)"')
        for i in re.findall(pattern,req.text):
            if i.find('http')!=-1:#有http->友情链接
                #webSiteSet.add(i)
                #print('友情链接',i) 
                #----------------------------------------------------------------------------#
                #友情链接还得处理 ->urlprase 看里面是否有注入点 如果有，去重扫描，并将域名丢到友情链接中等待扫描
                #----------------------------------------------------------------------------#
                self.friend_url.append(i)
            elif i.find('=')!=-1: #无参数
#                    i = self.url+i #带参数的链接
                self.format('http:'+self.url+i)
                    #print('带参数的链接'+self.url+i)
            else:
                #print('没用的url',i) #不带参数，无http关键词的链接
                pass
                
            #逻辑：href带http->友链
            #href不带http->有参数(=)->可能是payload，丢进去去重
            #href不带http->且无参数->无用url 直接丢弃
        for i in self.friend_url:
            print('友链',i)
        for i in self.testSet:
            print('可能存在payload的：',i)
    def parse_url(): #这是一个即将失效的方法
            fuck_set = set()
            url = ['http://www.hnfnu.edu.cn/NewsList.aspx?bbid=110&nid=10829','http://www.hnfnu.edu.cn/NewsList.aspx?bbid=111&nid=10835']
            for j in url:
                u = parse.urlparse(j)
                for i in u[4].split("&"):
                        print(i.split('=')[0])
                    #fuck_set.add(u[1]+u[2]+i.split('=')[0])
            #print(fuck_set)
    def format(self,url):
        '''
        策略是构建一个三元组
        第一项为url的netloc
        第二项为path中每项的拆分长度
        第三项为query的每个参数名称(参数按照字母顺序排序，避免由于顺序不同而导致的重复问题)'''
        save_url = url
        if urlparse.urlparse(url)[2] == '':
            url = url+'/'
        url_structure = urlparse.urlparse(url)
        netloc = url_structure[2]
        path = url_structure[2]
        query = url_structure[4]
        temp = (netloc,tuple([len(i) for i in path.split('/')]),tuple(sorted([i.split('=')[0] for i in query.split('&')])))
        #print temp, url
        str = ''
        for i in temp[2]:
            str = str+i+'&'
            if temp[0]+'?'+str in self.payload_url:
                print(url,'是一个重复的url')
                pass
            else: #不重复 特征值入set，url入set
                self.payload_url.add(temp[0]+'?'+str)
                self.testSet.add(url)
        #print(temp[0]+'?'+str)
        #return temp
a = BigFuck('http://www.hnfnu.edu.cn/')
a.get_things()
#parse_url('www.baidu.com/hello/fuck?a=2&h=000')
#print(__wooyun('www.baidu.com/hello/fuck?a=2&h=000'))
