import requests
import json
import time
import sqlite3
#这个类实现一个最简单的方法->给我一个url，我给你检测是否存在sql注入
#想法是 -> 让每个服务器都保持扫描10个线程的状态,很好解决
class ScanURL():
    """正在扫描的url的属性应该包含其url和扫描的大概时间"""
    def __init__(self,url,timeout):
        self.url = url
        self.timeout = timeout
        self.taskID = ''
if __name__=='__main__':
    conn = sqlite3.connect('hello.db')
    urlList = []
    host = 'http://nofiht.ml:8775'
    for url in conn.execute('select url from test where scaned=0').fetchall():
        url = url[0]
        if len(urlList)<5: #如果正在扫描的url数量小于10个，那么添加url 注：现更改为5个
            print(url)
            a = ScanURL(url,0)
            data = requests.get(host+'/task/new').json()
            if data['success']:
                a.taskID = data['taskid']
                r = requests.post(host+'/scan/%s/start'%a.taskID,data=json.dumps({'url':url},{'--'}),headers={'Content-Type':'application/json'})
                urlList.append(a)
            else:
                print('和远程服务器交互失败！请检查！')
            continue
        else: #如果现在要扫描的url等于5个，那么不停的检查
            for i in urlList:
                data = requests.get(host+'/scan/%s/status'%a.taskID).json()
                i.timeout = i.timeout+1
                time.sleep(10)
                if  data['status']=='terminated':
                    urlList.remove(i)
                    res = requests.get(host+'/scan/%s/data'%a.taskID).json()['data']
                    print(res)
                    if not res==[]: #data非空，存在sql注入
                        conn.execute('update test set Scaned=1,Payload=1 where url=?',(url,))
                        conn.commit()
                        print('经过sqlmap检查，这个url存在sql注入！'+'----'+url)
                        break
                    else:
                        conn.execute('update test set Scaned=1,Payload=0 where url=?',(url,))
                        conn.commit()
                        print('经过sqlmap检查，这个url不存在sql注入'+'-----'+url)
                        break
                    
                    urlList.remove(i)
                if i.timeout==3: #一次扫描 100s 两次 timeout=2 只给了一个url 100s的扫描时间 感觉有点不够 至少200s
                    urlList.remove(i)
                    conn.execute('update test set Scaned=-1 where url=?',(url,))
                    conn.commit()
                    requests.get(host+'/scan/%s/delete'%i.taskID)
                    print('成功删除一个不怎么带劲的IP'+url)
                else:
                    print(data)
                    
                    
                    
        # if data['success']:
            # #r = requests.post(host+'/scan/%s/start'%taskID,data=json.dumps({'url':url},{'--'}),headers={'Content-Type':'application/json'})
            # while(1):
                # data = requests.get(host+'/scan/%s/status'%taskID).json()
                # print(data)
                # if  data['status']=='terminated':
                    # res = requests.get(host+'/scan/%s/data'%taskID).json()['data']
                    # print(res)
                    # if not res==[]: #data非空，存在sql注入
                        # print('经过sqlmap检查，这个url存在sql注入！'+'----'+url)
                        # break
                    # else:
                        # print('经过sqlmap检查，这个url不存在sql注入'+'-----'+url)
                        # break
                # else:
                    # time.sleep(10)