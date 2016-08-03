import requests
import re
import sqlite3
from hashlib import _hashlib
import pymysql
import sys
from optparse import OptionParser
# 封装成类,搞定提示用户输入信息 编成class入队列
# 将要请求的http链接丢入队列中
########################################################################
class param_url:
    """带有参数的url类"""

    #----------------------------------------------------------------------
    def __init__(self, url, params): # 两个参数 自己的url和自己的参数 自己的参数是数组类型的
        """Constructor"""
        self.url = url
        self.params = params
    #----------------------------------------------------------------------
    def __str__(self):
        """return url"""
        return this.url
    
    
########################################################################
class Http():
    """给定的那个链接"""
    Scanedset = set() #已经扫描了的主站
    #----------------------------------------------------------------------
    def __init__(self, url):
        """Constructor"""
        self.url = url 
        self.scaned = 0
        self.good_url_list = []
        self.friend_url_set = set()
    
    #----------------------------------------------------------------------
    def is_good_url(self,url):
        """对有payload的url进行一个粗略的检测,例如存在jessonid这样的就返回false"""
        return True

    #----------------------------------------------------------------------
    def http_format(self, url):
        """格式化带有http的链接(外链),如果有注入点,丢到urllist中,然后将http://www.baidu.com这种格式丢进带扫描的队列"""
        # 单纯的只是友情链接
        try:
            self.friend_url_set.add('http://'+url.split('/')[2]+'/')
        except Exception as e:
            print('warning....http_format get an Exception－－>%s'%e)
     
    #----------------------------------------------------------------------
    def payload_format(self,url):
        """格式化带有=的链接"""
        return 1
    
    #----------------------------------------------------------------------
    def has_scand(self):
        """把扫描位置为1(已经扫描完成)"""   
        self.scaned = 1
        
    #----------------------------------------------------------------------
    def run(self):
        """找出这个链接中有效的url/网站"""
        """策略:每个带有http的链接的都格式化htpp://www.baidu.com/ 进入存储\
        对于有=的,只将本站找到的第一个有效链接存入对象中
        """
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko)'}
        try:
            req = requests.get(self.url,headers=header,timeout=3)
        except Exception as e:
            print(e)
            return
        
        pattern = re.compile('href="(.*?)"')
        for i in re.findall(pattern,req.text):
            if 'http' in i and i[0:4]=='http': # 标准的http友链地址
                self.http_format(i)
            elif '=' in i: # 只负责处理本链接带有参数的链接
                if not self.good_url_list:
                    if self.is_good_url(i):
                        self.good_url_list.append(self.url+i)
    #----------------------------------------------------------------------
    def read_db_mysql(self,conn):
        """从数据库中读取url进行扫描"""
        cur = conn.cursor()
    #----------------------------------------------------------------------
    def write_mysql(self,conn):
        """写入mysql的一个方法,和下面的writedb不正交"""
        """把对象的url和payload url 丢进database中"""   
        cur = conn.cursor()
        cur.execute('create table  if not exists payload_url(url varchar(108) primary key, from_url text, Scaned int,Payload int)')
        cur.execute('create table  if not exists friend_url(url varchar(108) primary key , Scaned int)')
        cur.execute('update friend_url set Scaned=1 where url=%s',(self.url))
        for i in self.good_url_list:# 有payload的url
            try:
                cur.execute('insert into payload_url values("%s","%s",%s,%s)',(i,self.url,0,0,))
            except pymysql.err.IntegrityError as e: # 已经存在列
                pass
        for i in self.friend_url_set:
            #cur.execute('insert into friend_url values("%s",%s)'%(i,0,))
            try:
                cur.execute('insert into friend_url values("%s",%s)'%(i,0,))
            except pymysql.err.IntegrityError as e: # 已经存在列
                pass
                #print(e)
                #print('出现错误,log如上,目测是已经存在列了,如果是因为已经存在了,那么你大可不必担心')
        conn.commit()        
        
    #----------------------------------------------------------------------
    def write_db(self,conn=sqlite3.connect('hello.db'),ismysql=0): 
        """为了兼容多种数据库使用的是conn对象-一个可以执行execute的游标
        当数据库为sqllite的时候直接给conn就好,
        当数据库为mysql的时候应该给cur = conn.cursor
        使用mysql以便于以后分布式的开发
        """
        """把对象的url和payload url 丢进database中"""
        #conn = sqlite3.connect('hello.db')
        conn.execute('create table  if not exists payload_url(url text primary key , from_url text, Scaned int,Payload int)')
        conn.execute('create table  if not exists friend_url(url text primary key, Scaned int)')
        for i in self.good_url_list:# 有payload的url
            try:
                conn.execute('insert into payload_url values(?,?,?,?)',(i,self.url,0,0,))
            except Exception as e:
                print(e)
                print('出现错误如上,可能是IntergerityError,大可不必惊慌')
        for i in self.friend_url_set:
            try:
                conn.execute('insert into friend_url values(?,?)',(i,0,))
            except Exception as e:
                print(e)
                print('出现错误,log如上,目测是已经存在列了,如果是因为已经存在了,那么你大可不必担心')
        conn.commit()
        #conn.close()
    #----------------------------------------------------------------------
    def print_details(self,v):
        """打印这个对象的各种属性"""
        print('正在检测的url->%s'%self.url)
        if v==0: # 打印两个属性
            print('找到了%d个友情链接'%len(self.friend_url_set))
            print('本地有payload的链接->%s'%self.good_url_list)
        if v==1: # 打印两个属性 并且打印出友情链接
            print('找到了%d个友情链接'%len(self.friend_url_set))
            print('本地有payload的链接->%s'%self.good_url_list)
            print('%s下的友情链接'%self.url)
            for i in self.friend_url_set:
                print(i)
            
    #----------------------------------------------------------------------
    def __hash__(self):
        """返回hash值,丢进set中"""
        return hash(self.url)
        
########################################################################
class ScanUtil:
    """一个扫描的工具类,用来驱动http类"""
    #----------------------------------------------------------------------
    def read_db(count=10,conn = sqlite3.connect('hello.db')):
        """从数据库里面读取count个url然后进行扫描"""
        for url in conn.execute('select url from friend_url where Scaned=0 limit ? ',(count,)).fetchall():
            ScanUtil.Scan(url[0],print=0)
            conn.execute('update friend_url set Scaned=1 where url=?',(url[0],))
        conn.commit()
        conn.close()
    #----------------------------------------------------------------------
    def read_db_mysql(conn,count=10):
        """从mysql中读取count个url然后扫描"""
        cur = conn.cursor()
        sql = 'select url from friend_url where Scaned=0 limit %s'
        cur.execute(sql,(count))
        for url in cur:
            print(url[0])
            ScanUtil.Scan(url[0],conn,print=0)
        conn.close()
    #----------------------------------------------------------------------
    def Scan_newer(url):
        """Scan and print"""
        a = Http(url)
        a.run()
        a.print_details(1)
        return a
    #----------------------------------------------------------------------
    def Scan(url,conn,print=1):
       # """扫描指定的url"""
        a = Http(url)
        a.run()
        if print:
            a.print_details(1)
        else:
            #conn=pymysql.connect(host='localhost',user='root',passwd='fang328915',db='test')
            a.write_mysql(conn)
            #print('成功写入数据库!')
    #----------------------------------------------------------------------
    def Scantest(a):
        """用来测试实际效果的方法"""
        a.run()
        for i in a.friend_url_set:
            jj = Http(i)
            jj.run()
            #jj.print_details(0)
            jj.write_db()

    #----------------------------------------------------------------------
    def scan_count_url(url,count):
        """要求是找到count个带有payload的url"""
        purl_list = []
        
        
if __name__=='__main__':
    #ScanUtil.Scan('http://www.sdu.edu.cn/',0)
    ScanUtil.Scantest(Http('http://www.ujn.edu.cn/'))
    #conn=pymysql.connect(host='localhost',user='root',passwd='fang328915',db='test')
    # for i in range(100):
        # ScanUtil.read_db_mysql(conn,count=100)

# if __name__=='__main__':
    # parser = OptionParser('AutoSql by fiht')
    # parser.add_option('-m','--mysql',dest='mysql',help='use mysql save the result')
    # parser.add_option('-u','--url',dest='target',help='the target')
    # parser.add_option('-n','--number',dest='num',help='friend_url\'s num you wanner get')
    # parser.add_option('-p','--payload',dest='purl_num',help='friend')
    # parser.add_option('-a','--auto',dest='auto',help='auto scan,let you database bigger!')
    # (options ,args) = parser.parse_args()
    # if not (options.target or options.auto):
        # parser.print_help()
        # sys.exit(0)
    # if options.target and options.num:
        # ScanUtil.Scan_newer(options.target)
    # print(args)
"""
to do
优化程序结构
对于
http://021.qeo.cn/
http://023.qeo.cn/
http://024.qeo.cn/
http://025.qeo.cn/
http://027.qeo.cn/
http://028.qeo.cn/
http://029.qeo.cn/
http://0311.qeo.cn/
http://0371.qeo.cn/
http://0411.qeo.cn/
http://0510.qeo.cn/
这么变态的网址列表．．．应该检测ｉｐ地址然后再选择是否存入数据库
"""