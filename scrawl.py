# -*- coding: utf-8 -*-

from datetime import datetime
import core
import db

if __name__=="__main__":
    regionlist = [u'xicheng', u'dongcheng', u'haidian', u'chaoyang']    # only pinyin support

    dbflag = 'local'            # local,  remote
    conn = db.database_init(dbflag)
    print "获取小区信息"
    core.GetCellByRegionlist(conn,regionlist)         # init,scrapy celllist and insert database; could run only 1st time
    starttime = datetime.now()
    celllist = db.get_celllist(conn)    #  read celllist from database
    # myfavor = [u'蓝色家族',u'望京明苑',u'星源国际',u'',u'银领国际',u'望京西园三区',u'望京西园一区']
    # for x in myfavor:
    #     celllist.append(x)
    # celllist[1793:-6]=[]
    # print "获取房屋信息"
    #core.GetHouseByCelllist(conn,celllist)
    conn.close()
    endtime =  datetime.now()
    print(u'the house spider time is ' + str(endtime-starttime))
