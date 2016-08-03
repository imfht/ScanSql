import requests
from bs4 import BeautifulSoup
import time
import queue
import threading
import os
import sys
from optparse import OptionParser
#----------------------------------------------------------------------
"""return None 有点问题,但是不想折腾了"""
def get_subDomain(url):
    """返回子域名list"""
    try:
        req =requests.post('http://i.links.cn/subdomain/',data='domain=%s&b2=1&b3=1&b4=1'%url,headers={'Content-Type': 'application/x-www-form-urlencoded'},timeout=10)
    except Exception as e:
        print(e)
        return None
    return_value = []
    sub_domains = BeautifulSoup(req.text,'lxml').findAll(rel='nofollow')
    if len(sub_domains)==2:
        return_value.append(url)
        return return_value
    for i in sub_domains:
        return_value.append(i.string)
    print(url,'寻找完毕')
    return return_value
que = queue.Queue()
target = ''
#----------------------------------------------------------------------
def run_thread():
    """"""
    while(not que.empty()):
        url = que.get()
        sub_domains = get_subDomain(url)
        if not sub_domains: # 返回None
            print('%url 返回了个空,我也不知道为什么,也不愿意给你解决')
        else:
            for i in sub_domains:
                print(i,file=target)
#----------------------------------------------------------------------
if __name__=='__main__':
    """"""
    parser = OptionParser()
    if len(sys.argv) < 2:
        print("介绍:python3 get_subDomain 文件路径")
        print('然后程序就会给你找出 文件中所有域名的子域名 并保存为文件名_subDomains')        
        print('请输入文件名')
        sys.exit(0)
    an_loney_list = []
    print('正在寻找,默认开启100个线程,需要的自己加')
    target = open(sys.argv[1]+'subDomain','w+')
    with open(sys.argv[1]) as e:
        for i in e.readlines():
            i = i.strip('\n')
            if i not in an_loney_list: # 主要是去重
                an_loney_list.append(i)
                #print(i)
            else:
                #print('发现一个重复的->',i)
                pass
    for i in an_loney_list:
        que.put(i)
    threads = [threading.Thread(target=run_thread) for i in range(0,100)]
    for i in threads:
        i.start()
        i.join()