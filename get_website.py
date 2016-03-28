import requests
import re
from urllib import parse
from bs4 import BeautifulSoup

def Fuck_Href(href):
    pattern = re.compile('site_(.*?)\.html')
    return re.findall(pattern,href)[0]
def Fuck_main(keyWord): # this is the fuck main
    req = requests.get("http://search.top.chinaz.com/Search.aspx?p=1&url="+str(keyWord))
    pattern = re.compile("相关的结果(.*?)条")
    print(re.findall(pattern,req.text)[0])
    page = int(int(re.findall(pattern,req.text)[0])/30)+1
    print(page)
    for i in range(1,page+1):
        soup = BeautifulSoup(req.text,'html.parser')
        for j in soup.findAll(class_='pr10 fz14'):#print(i.getText()) #打印名字
            print(Fuck_Href(j['href']),j.text)
        req = requests.get("http://search.top.chinaz.com/Search.aspx?p=%d&url="%i+str(keyWord))
Fuck_main("p2p")
