import core
import db

if __name__=="__main__":
    regionlist = [u'chaoyang', u'dongcheng', u'xicheng', u'haidian'] # only pinyin support

    dbflag = 'local' # local,  remote
    conn = db.database_init(dbflag)
    #core.GetCellByRegionlist(conn,regionlist) # Init,scrapy celllist and insert database; could run only 1st time
    celllist = db.get_celllist(conn) # Read celllist from database
    #core.GetHouseByCelllist(conn,celllist)
    core.GetSellByCelllist(conn, celllist)
    conn.close()
