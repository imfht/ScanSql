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
    
    #----------------------------------------------------------------------
    def __init__(self, url,):
        """Constructor"""
        self.url = url 
        self.scaned = 0
        self.good_url_list = []
        self.friend_url_list = []
    #----------------------------------------------------------------------
    def is_good_url(url):
        """对有payload的url进行一个粗略的检测,例如存在jessonid这样的就返回false"""
        return True

    #----------------------------------------------------------------------
    def http_format(self, url):
        """格式化带有http的链接(外链),如果有注入点,丢到urllist中,然后将http://www.baidu.com这种格式丢进带扫描的队列"""
        if(url.find('=')!=-1): # 存在'='视为带有payload的链接
            if is_good_url(url):
                self.url_param.append(url)
        else: # 单纯的只是友情链接
            self.friend_url_list.append(i)
    #----------------------------------------------------------------------
    def run(self):
        """找出这个链接中有效的url/网站"""
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko)'}
        try:
            req = requests.get(self.url,headers=header,timeout=3)
        except Exception as e:
            print(e)
            return
        pattern = re.compile('href="(.*?)"')
        for i in re.findall(pattern,req.text):
            if 'http' in i and i[0:4]=='http': # 标准的http友链地址
                http_format(i)
            elif '=' in i: # 只负责处理本链接带有参数的链接
