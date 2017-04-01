import mysql.connector
import misc

def database_init(dbflag='local'):
     if dbflag == 'local':
         conn = mysql.connector.connect(user='root', password='', database='lianjiaSpider', host='127.0.0.1')
     else:
         conn = mysql.connector.connect(user='user', password='password', database='lianjia', host='lianjia')
     dbc = conn.cursor()

     # create houseinfo and hisprice table:
     dbc.execute('create table if not exists houseinfo (id int(10) NOT NULL AUTO_INCREMENT primary key,houseID varchar(50) , Title varchar(200), link varchar(200), cellname varchar(100),\
                years varchar(200),housetype varchar(50),square varchar(50), direction varchar(50),floor varchar(50),taxtype varchar(200), \
                totalPrice varchar(200), unitPrice varchar(200),followInfo varchar(200),validdate varchar(50),validflag varchar(20))')

     dbc.execute('create table if not exists hisprice (id int(10) NOT NULL AUTO_INCREMENT primary key,houseID varchar(50) , date varchar(50), totalPrice varchar(200))')
     dbc.execute('create table if not exists cellinfo (id int(10) NOT NULL AUTO_INCREMENT primary key,Title varchar(50) , link varchar(200),district varchar(50),bizcircle varchar(50),tagList varchar(200))')

     conn.commit()
     dbc.close()
     return conn

def celllist_init(conn):
    cursor = conn.cursor()
    #all set unvaild
    cursor.execute('update houseinfo set validflag= %s',('0',))
    conn.commit()
    cursor.close()

def get_celllist(conn):
    cursor = conn.cursor()
    cursor.execute('select * from cellinfo ')
    values = cursor.fetchall()         #turple type

    celllist = []
    for j in range(len(values)):
        celllist.append(values[j][1])

    return celllist

def update_cellinfo(conn,info_dict):

    t = (info_dict[u'Title'],info_dict[u'link'],info_dict[u'district'],info_dict[u'bizcircle'],info_dict[u'tagList'])  # for cellinfo

    cursor = conn.cursor()

    cursor.execute('select * from cellinfo where Title = (%s)',(info_dict[u'Title'],))
    values = cursor.fetchall()         #turple type

    if len(values) == 0:        # new cell
        cursor.execute('insert into cellinfo (Title,link,district,bizcircle,tagList) values (%s,%s,%s,%s,%s)', t)
    else:
        cursor.execute('update cellinfo set link = %s,district = %s, bizcircle = %s,tagList = %s where Title = %s',\
                       (info_dict[u'link'],info_dict[u'district'],info_dict[u'bizcircle'],info_dict[u'tagList'],info_dict[u'Title']))

    conn.commit()
    cursor.close()

def update_houseinfo(conn,info_dict):
    info_list = [u'houseID',u'Title',u'link',u'cellname',u'years',u'housetype',u'square',u'direction',u'floor',\
                u'taxtype',u'totalPrice',u'unitPrice',u'followInfo',u'validdate',u'validflag']
    t = []
    for il in info_list:
        if il in info_dict:
            t.append(info_dict[il])
        else:
            t.append('')
    t = tuple(t)    # for houseinfo

    today = misc.get_today()
    t2 = (info_dict[u'houseID'],today,info_dict[u'totalPrice'])  # for hisprice

    cursor = conn.cursor()

    cursor.execute('select * from houseinfo where houseID = (%s)',(info_dict[u'houseID'],))
    values = cursor.fetchall()         #turple type
    if len(values)>0:
        nvs = zip(info_list,list(values[0][1:]))
        Qres = dict( (info_list,value) for info_list,value in nvs)
    else:
        pass

    if len(values) == 0:        # new house
        cursor.execute('insert into houseinfo (houseID,Title,link,cellname,years,housetype,square,direction,floor,\
                      taxtype,totalPrice,unitPrice,followInfo,validdate,validflag) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', t)
        cursor.execute('insert into hisprice (houseID,date,totalPrice) values (%s,%s,%s)', t2)
    else:
        cursor.execute('update houseinfo set totalPrice = %s,unitPrice = %s,followInfo = %s,validdate = %s,\
                       validflag= %s where houseid = %s',(info_dict[u'totalPrice'],info_dict[u'unitPrice'],\
                                                          info_dict[u'followInfo'],today,'1',info_dict[u'houseID']))

        if int(today) > int(Qres[u'validdate']):
            cursor.execute('insert into hisprice (houseID,date,totalPrice) values (%s,%s,%s)', t2)
        else:
#            cursor.execute('update houseinfo set validflag= %s where houseid = %s',('1',info_dict[u'houseID']))
            cursor.execute('update hisprice set totalPrice= %s where houseid = %s',(info_dict[u'totalPrice'],info_dict[u'houseID']))
        if float(Qres[u'totalPrice']) != float(info_dict[u'totalPrice']):    # str2float,when str2int is error
            info_dict[u'oldprice'] = Qres[u'totalPrice']
#            trigger_notify_email(info_dict,'updateprice')

    conn.commit()
    cursor.close()
    