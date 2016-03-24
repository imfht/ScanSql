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
    def get_things(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text,'lxml')
        #print(req.text)
        pattern = re.compile('href="(.*?)"')
        for i in re.findall(pattern,req.text):
            #print(i)
            if i.find('=')!=-1:
                if i.find('http'):
                    i = self.url+i
                
            #if i['href'].find('http')!=-1:
                #webSiteSet.add(i['href'])
            #else:
                #print(i['href'])
            #存在href中存在http标记的即为友情链接
            #不存在href的即为非友情链接（是否存在url参数以检索payload）
        #print(req.text)
        #for i in webSiteSet:
            #print(i)
def parse_url():
    fuck_set = set()
    url = ['http://www.hnfnu.edu.cn/NewsList.aspx?bbid=110&nid=10829','http://www.hnfnu.edu.cn/NewsList.aspx?bbid=111&nid=10835']
    for j in url:
        u = parse.urlparse(j)[4]
        for i in u.split("&"):
            #print(i.split('=')[0])
            fuck_set.add(i.split('=')[0])
    print(fuck_set)
#a = BigFuck('http://www.hnfnu.edu.cn/')
#a.get_things()
parse_url()