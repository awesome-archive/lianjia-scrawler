# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import db
import misc
import time
import datetime
import urllib2

def GetHouseByCelllist(conn,celllist=[u'荣丰2008',u'保利茉莉公馆']):
    db.celllist_init(conn)
    for cellname in celllist:
        try:
            get_house_percell(conn,cellname)
            print cellname + u"搜索完成"
        except Exception as e:
            print (e)
            print cellname + u"搜索失败"
            pass
    #return house         # unit test

def GetChengjiaoByCelllist(conn,celllist=[u'荣丰2008',u'保利茉莉公馆']):
    db.celllist_init(conn)
    for cellname in celllist:
        try:
            get_chengjiao_percell(conn,cellname)
            print cellname + u"搜索完成"
        except Exception as e:
            print (e)
            print cellname + u"搜索失败"
            pass
    #return house         # unit test

def GetCellByRegionlist(conn,regionlist = [u'xicheng']):
    for regionname in regionlist:
        try:
            get_cell_perregion(conn,regionname)
            print regionname + u"搜索完成"
            #celldict = cell_perregion_spider(conn,regionname)
        except Exception as e:
            print (e)
            print regionname + u"搜索失败"
            pass 
#    return celldict       # only unit test

def get_house_percell(conn, cellname=u'荣丰2008'):
    url = u"http://bj.lianjia.com/ershoufang/rs" + urllib2.quote(cellname.encode('utf8')) + "/"
    source_code = misc.get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')
    total_pages = misc.get_total_pages(url)
    info_dict_all = {}   # if each house info_dict insert into database ,this info_dict_all is not needed
    for page in range(total_pages):
        if page > 0:
            url_page = u"http://bj.lianjia.com/ershoufang/pg%drs%s/" % (page+1, urllib2.quote(cellname.encode('utf8')))
            source_code = misc.get_source_code(url_page)
            soup = BeautifulSoup(source_code, 'lxml')

        nameList = soup.findAll("li", {"class":"clear"})
        i = 0

        for name in nameList:   # per house loop
            i = i + 1
            info_dict = {}
            info_dict_all.setdefault(i+page*30, {})

            housetitle = name.find("div", {"class":"title"})  #html
            info_dict.update({u'Title':housetitle.get_text().strip()})
            info_dict.update({u'link':housetitle.a.get('href')})   #atrribute get

            houseaddr = name.find("div", {"class":"address"})
            info = houseaddr.div.get_text().split('|')
            info_dict.update({u'cellname':info[0]})
            info_dict.update({u'housetype':info[1]})
            info_dict.update({u'square':info[2]})
            info_dict.update({u'direction':info[3]})

            housefloor = name.find("div", {"class":"flood"})
            floor_all = housefloor.div.get_text().split('-')[0].strip().split(' ')
            info_dict.update({u'floor':floor_all[0]})
            info_dict.update({u'years':floor_all[-1]})

            followInfo = name.find("div", {"class":"followInfo"})
            info_dict.update({u'followInfo':followInfo.get_text()})

            tax = name.find("div", {"class":"tag"})
            info_dict.update({u'taxtype':tax.get_text().strip()})   # none span
            #info_dict.update({u'taxtype':tax.span.get_text()})

            totalPrice = name.find("div", {"class":"totalPrice"})
            info_dict.update({u'totalPrice':totalPrice.span.get_text()})

            unitPrice = name.find("div", {"class":"unitPrice"})
            info_dict.update({u'unitPrice':unitPrice.get('data-price')})
            info_dict.update({u'houseID':unitPrice.get('data-hid')})

            today = misc.get_today()
            info_dict.update({u'validdate':today})
            info_dict.update({u'validflag':str('1')})

            # adding open houseid url,and save the images for each house,TBC


            # houseinfo insert into mysql
            db.update_houseinfo(conn,info_dict)

            info_dict_all[i+page*30] = info_dict
            time.sleep(1)

    return info_dict_all

def get_chengjiao_percell(conn, cellname=u'荣丰2008'):
    url = u"http://bj.lianjia.com/chengjiao/rs" + urllib2.quote(cellname.encode('utf8')) + "/"
    source_code = misc.get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')
    total_pages = misc.get_total_pages(url)
    info_dict_all = {}   # if each house info_dict insert into database ,this info_dict_all is not needed
    for page in range(total_pages):
        if page > 0:
            url_page = u"http://bj.lianjia.com/chengjiao/pg%drs%s/" % (page+1, urllib2.quote(cellname.encode('utf8')))
            source_code = misc.get_source_code(url_page)
            soup = BeautifulSoup(source_code, 'lxml')
        i = 0
        for ultag in soup.findAll("ul", {"class":"listContent"}):
            for name in ultag.find_all('li'):
                i = i + 1
                info_dict = {}
                info_dict_all.setdefault(i+page*30, {})

                housetitle = name.find("div", {"class":"title"})  #html
                info_dict.update({u'Title':housetitle.get_text().strip()})
                info_dict.update({u'link':housetitle.a.get('href')})   #atrribute get
                houseID = int(housetitle.a.get('href').split("/")[-1].split(".")[0])
                info_dict.update({u'houseID':houseID})

                house = housetitle.get_text().strip().split(' ')
                info_dict.update({u'cellname':house[0]})
                info_dict.update({u'housetype':house[1]})
                info_dict.update({u'square':house[2]})

                houseinfo = name.find("div", {"class":"houseInfo"})
                info = houseinfo.get_text().split('|')
                info_dict.update({u'direction':info[0]})
                info_dict.update({u'status':info[1]})

                housefloor = name.find("div", {"class":"positionInfo"})
                floor_all = housefloor.get_text().strip().split(' ')
                info_dict.update({u'floor':floor_all[0]})
                info_dict.update({u'years':floor_all[-1]})

                followInfo = name.find("div", {"class":"source"})
                info_dict.update({u'source':followInfo.get_text()})

                totalPrice = name.find("div", {"class":"totalPrice"})
                info_dict.update({u'totalPrice':totalPrice.span.get_text()})

                unitPrice = name.find("div", {"class":"unitPrice"})
                info_dict.update({u'unitPrice':unitPrice.span.get_text()})

                dealDate= name.find("div", {"class":"dealDate"})
                info_dict.update({u'dealdate':dealDate.get_text()})
                info_dict.update({u'validflag':str('1')})
                
                today = misc.get_today()
                info_dict.update({u'updatedate':today})

                # houseinfo insert into mysql
                db.update_chengjiaoinfo(conn,info_dict)

                info_dict_all[i+page*30] = info_dict
                time.sleep(1)


    return info_dict_all

def get_cell_perregion(conn, regionname=u'xicheng'):
    url = u"http://bj.lianjia.com/xiaoqu/" + regionname +"/"
    source_code = misc.get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')
    total_pages = misc.get_total_pages(url)
    info_dict_all = {}   # if each house info_dict insert into database ,this info_dict_all is not needed

    for page in range(total_pages):
        if page > 0:
            url_page = u"http://bj.lianjia.com/xiaoqu/" + regionname +"/pg%d/" % (page+1,)
            source_code = misc.get_source_code(url_page)
            soup = BeautifulSoup(source_code, 'lxml')

        nameList = soup.findAll("li", {"class":"clear"})
        i = 0

        for name in nameList:   # per house loop
            i = i + 1
            info_dict = {}
            info_dict_all.setdefault(i+page*30, {})

            celltitle = name.find("div", {"class":"title"})  #html
            info_dict.update({u'Title':celltitle.get_text().strip('\n')})
            info_dict.update({u'link':celltitle.a.get('href')})   #atrribute get

            district = name.find("a", {"class":"district"})  #html
            info_dict.update({u'district':district.get_text()})
            bizcircle = name.find("a", {"class":"bizcircle"})
            info_dict.update({u'bizcircle':bizcircle.get_text()})

            tagList = name.find("div", {"class":"tagList"})
            info_dict.update({u'tagList':tagList.get_text().strip('\n')})

            # cellinfo insert into mysql
            db.update_cellinfo(conn,info_dict)

            info_dict_all[i+page*30] = info_dict
            time.sleep(1)

#    return info_dict_all    #only for unit test
