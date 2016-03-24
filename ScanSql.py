import re
from bs4 import BeautifulSoup
import requests
from urllib import parse
webSiteSet = set()
class WebSite():
    #一个WebSite应该有的属性 
    def __init__(self,name,url):
        self.name = name
        self.url = url
        self.payload = []
    def put_link(self,url):
        self.set.add(url)
class BigFuck():
    def __init__(self,url):
        self.url = url
        self.friend_url = []
        self.payload_url = []
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
                self.payload_url.append(self.url+i)
                    #print('带参数的链接'+self.url+i)
            else:
                #print('没用的url',i) #不带参数，无http关键词的链接
                pass
                
            #逻辑：href带http->友链
            #href不带http->有参数(=)->可能是payload，丢进去去重
            #href不带http->且无参数->无用url 直接丢弃
        for i in self.friend_url:
            print('友链',i)
        for i in self.payload_url:
            print('可能存在payload的链接',i)
def parse_url():
    fuck_set = set()
    url = ['http://www.hnfnu.edu.cn/NewsList.aspx?bbid=110&nid=10829','http://www.hnfnu.edu.cn/NewsList.aspx?bbid=111&nid=10835']
    for j in url:
        u = parse.urlparse(j)[4]
        for i in u.split("&"):
            #print(i.split('=')[0])
            fuck_set.add(i.split('=')[0])
    print(fuck_set)
a = BigFuck('http://www.hnfnu.edu.cn/')
a.get_things()