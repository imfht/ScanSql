import re
import requests
from urllib import parse
import urllib.parse as urlparse
import queue
import sys
webSiteSet = set()
fuck_set = set()
dic = {}
http_dic = {}
class attack_url():
    def __init__(self,www_path,param):
        self.www_path = www_path.lower()
        self.param = param #参数
    def __hash__(self):
        return hash(self.www_path)
class BigFuck():
    def __init__(self,url):
        self.dic = {}
        self.url = url
        self.friend_url = set()
        self.payload_url = set()
        self.attach_url = queue.Queue()
        self.testSet = set()
    def get_things(self):
        try:
            req = requests.get(self.url,timeout=3)
            #print('连接到网站 正在分析中...')
            #soup = BeautifulSoup(req.text,'lxml')
            #print(req.text)
            pattern = re.compile('href="(.*?)"')
            for i in re.findall(pattern,req.text):
                has_http = i.find('http')!=-1
                has_flag = i.find('=')!=-1
                
                if has_flag: #有参数的链接
                    if(has_http):
                        self.my_format(i)
    #                    i = self.url+i #带参数的链接
                    else:
                        self.my_format(self.url+i)
                        #print('带参数的链接'+self.url+i)
                if has_http:#有http->友情链接
                    self.http_format(i)
                    #self.friend_url.add(i)
                else:
                    #print('没用的url',i) #不带参数，无http关键词的链接
                    pass
                #逻辑：href带http->友链
                #href不带http->有参数(=)->可能是payload，丢进去去重
                #href不带http->且无参数->无用url 直接丢弃
            #for i in self.friend_url:
            #    print('友情链接',i)
            #for i in self.testSet: #for format
                #print('可能存在payload的：',i)
            
            #for i in self.friend_url:
                #self.url=i
                #self.get_things()
            #print('----------over-------------')
        except Exception:
            #print('连接到指定网站失败')
            pass
    def http_format(self,url):
        #print(url,'---->')
        """用来格式化http链接的util类"""
        www_path = url[0:url.rfind('/')]
        if www_path not in http_dic:
            http_dic[www_path] = url
        else:
            pass
            #print('找到一个重复的url',url)
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
                #print(url,'是一个重复的url')
                pass
            else: #不重复 特征值入set，url入set
                self.payload_url.add(temp[0]+'?'+str)
                self.testSet.add(url)
        #print(temp[0]+'?'+str)
        #return temp
    def my_format(self,url):
        #print('正在检测',url)
        url_seq = parse.urlparse(url)
        str = [tuple(sorted(i.split('=')[0] for i in url_seq[4].split('&')))] #排好序的参数
        Attack_url = attack_url(url_seq[1]+url_seq[2],str)
        if Attack_url in dic:
            for i in str:
                if i not in dic[Attack_url.www_path]:#应该取参数最多的那个
                    if len(str) > len(dic[Attack_url.www_path].params):
                        dic[Attack_url.www_path].update = url
        else:
            dic[Attack_url.www_path] = url
        #print(dic)
"""下面BigFuck的参数即为扫描目标，可自由制定，别忘了加http哦!"""
if len(sys.argv)>1:
    a = BigFuck(sys.argv[1])
    print('Scaning ',a.url)
else:
    a = BigFuck('http://www.sdu.edu.cn')
"""上面BigFuck的参数即为扫描目标，可自由制定，别忘了加http哦!"""
a.get_things()
http_dic_clone = http_dic.copy()
for i in http_dic_clone:
    a = BigFuck(http_dic[i])
    a.get_things()
#for i in http_dic:
#    print('友情链接：',http_dic[i])
for i in dic:
    if(dic[i].find('youku')==-1&dic[i].find('filename')==-1):
        print(dic[i])
#parse_url('www.baidu.com/hello/fuck?a=2&h=000')
#print(__wooyun('www.baidu.com/hello/fuck?a=2&h=000'))


