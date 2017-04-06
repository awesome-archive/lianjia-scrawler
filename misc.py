# -*- coding: utf-8 -*-
import requests
import random
from datetime import datetime
from bs4 import BeautifulSoup

hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

#=========================Add proxy to prevent lianjia blocking=========================================
# s = requests.Session()
# proxies = {
#         'http': 'http://127.0.0.1:8087',
#         'https': 'http://127.0.0.1:8087',
# }
hd = {
    'Host': 'bj.lianjia.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'http://captcha.lianjia.com/?redirect=http%3A%2F%2Fbj.lianjia.com%2Fxiaoqu%2Fxicheng%2F',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cookie': 'all-lj=ae53ba2bb01d9055b48cc0081f0ce3f9; lianjia_uuid=eb8ad88b-51b6-4536-b30e-8510f5095a31; UM_distinctid=15b2e967f0425b-058036b3f786e6-1d3a6853-1fa400-15b2e967f053e4; select_city=110000; _smt_uid=58e0eb23.419cbb57; CNZZDATA1253477573=705813043-1491130452-null%7C1491227721; CNZZDATA1254525948=720754788-1491131771-null%7C1491224601; CNZZDATA1255633284=713550089-1491131528-null%7C1491225849; CNZZDATA1255604082=665248520-1491130401-null%7C1491227607; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _ga=GA1.2.1914918537.1491135269; _gat_dianpu_agent=1; lianjia_ssid=989fe080-a977-4731-b889-db15c1db5347'
    }

def get_today():
    now = datetime.now()
    m = now.month
    d = now.day
    if m < 10:
        ms = '0' + str(m)
    else:
        ms = str(m)
    if d < 10:
        ds = '0' + str(d)
    else:
        ds = str(d)
    today = str(now.year) + ms + ds
    return today

def get_source_code(url):
    try:
        #req = urllib2.Request(url, headers=hds[random.randint(0,len(hds)-1)])
        #source_code = urllib2.urlopen(req, timeout=10).read()
        result = requests.get(url, headers=hd)
        source_code = result.content
    except Exception as e:
        print (e)
        return

    soup = BeautifulSoup(source_code, "html.parser")

    try:
        error = soup.title.text
        if error == u"验证异常流量-链家网":
            print u'ip被封 请尝试更换代理'
            return
        else:
            pass
    except:
        pass

    return source_code

def get_total_pages(url):
    source_code = get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')
    total_pages = 0
    try:
        page_info = soup.find('div',{'class':'page-box house-lst-page-box'})
    except AttributeError as e:
        page_info = None

    if page_info == None:
        print "Lianjia block us:("
        return None
    page_info_str = page_info.get('page-data').split(',')[0]  #'{"totalPage":5,"curPage":1}'
    total_pages = int(page_info_str.split(':')[1])
    return total_pages
    