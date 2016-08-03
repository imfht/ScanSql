#!/usr/bin/python
#-*-coding:utf-8-*-
import requests
import time
#import pymysql
import json
import sqlite3
#conn = sqlite3.connect('hello.db')
class AutoSqli(object):

    """
    使用sqlmapapi的方法进行与sqlmapapi建立的server进行交互

    By Manning
    """

    def __init__(self, Server , target='',data = '',referer = '',cookie = ''):
        super(AutoSqli, self).__init__()
        self.server = Server.server
        Server.count = Server.count + 1
        if self.server[-1] != '/':
            self.server = self.server + '/'
        self.target = target
        self.taskid = ''
        self.engineid = ''
        self.status = ''
        self.data = data
        self.referer = referer
        self.cookie = cookie
        self.start_time = time.time()

    #新建扫描任务
    def task_new(self):
        self.taskid = json.loads(
            requests.get(self.server + 'task/new').text)['taskid']
        print('Created new task: ' + self.taskid)
        #得到taskid,根据这个taskid来进行其他的
        if len(self.taskid) > 0:
            return True
        return False

    #删除扫描任务
    def task_delete(self):
        if json.loads(requests.get(self.server + 'task/' + self.taskid + '/delete').text)['success']:
            print ('[%s] Deleted task' % (self.taskid))
            return True
        return False

    #扫描任务开始
    def scan_start(self):
        headers = {'Content-Type': 'application/json'}
        #需要扫描的地址
        payload = {'url': self.target}
        url = self.server + 'scan/' + self.taskid + '/start'
        #http://127.0.0.1:8557/scan/xxxxxxxxxx/start
        t = json.loads(
            requests.post(url, data=json.dumps(payload), headers=headers).text)
        self.engineid = t['engineid']
        if len(str(self.engineid)) > 0 and t['success']:
            print ('Started scan')
            return True
        return False

    #扫描任务的状态
    def scan_status(self):
        self.status = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/status').text)['status']
        if self.status == 'running':
            return 'running'
        elif self.status == 'terminated':
            return 'terminated'
        else:
            return 'error'

    #扫描任务的细节
    def scan_data(self):
        self.data = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/data').text)['data']
        print('--->',self.data)
        if len(self.data) == 0:
            print ('not injection:\t')

        else:
            print ('injection:\t' + self.target)

    #扫描的设置,主要的是参数的设置
    def option_set(self):
        headers = {'Content-Type': 'application/json'}
        option = {"options": {
                    "smart": False,
                    }
                 }
        url = self.server + 'option/' + self.taskid + '/set'
        t = json.loads(
            requests.post(url, data=json.dumps(option), headers=headers).text)
        print(t)

    #停止扫描任务
    def scan_stop(self):
        json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/stop').text)['success']

    #杀死扫描任务进程
    def scan_kill(self):
        json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/kill').text)['success']

    def run(self):
        if not self.task_new():
            return False
        self.option_set()
        if not self.scan_start():
            return False
        while True:
            if self.scan_status() == 'running':
                time.sleep(10)
            elif self.scan_status() == 'terminated':
                break
            else:
                break
            print (time.time() - self.start_time)
            if time.time() - self.start_time > 30000:
                error = True
                self.scan_stop()
                self.scan_kill()
                break
        self.scan_data()
        self.task_delete()
        print (time.time() - self.start_time)
########################################################################
class Server():
    """一个节点记为一个host"""

    #----------------------------------------------------------------------
    def __init__(self, server):
        """Constructor"""
        self.server = server
        self.count = 0
        
    
if __name__ == '__main__':
    serverList = [Server('http://127.0.0.1:8775')]
    AutoSqli(serverList[0],target='http://e085498ac408a3614.jie.sangebaimao.com/mysql/get_str_like_par2.php?id=1').run()
    