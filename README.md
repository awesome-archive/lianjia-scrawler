# lianjia-scrawler
This repo provides a tool to scrawl house info at LianJia.com. The data will be stored in Mysql datatbase. It will be easy to export to CSV or other formates. You also can [sync Mysql to Elasticsearch](https://github.com/siddontang/go-mysql-elasticsearch). In this way, you can use [kibana](https://github.com/elastic/kibana) to analyse these data.

This tool could collect cellname from each region at first, then you'd like to use these cellnames to learn about onsale, history price, sold and rent information.

## Usage
+ Download source code and install package dependency. 
```
1. git clone https://github.com/XuefengHuang/lianjia-scrawler.git
2. cd lianjia-scrawler
# If you'd like not to use [virtualenv](https://virtualenv.pypa.io/en/stable/), please skip step 3 and 4.
3. virtualenv lianjia
4. source lianjia/bin/activate
5. pip install -r requirements.txt
```
+ Setting DB config at config.ini
```
[mysql]
scheme = test
host = 127.0.0.1
port = 3306
user = root
password = 123456
```

+ Please add your favor region at scrawl.py `regionlist = [u'chaoyang', u'xicheng', u'dongcheng'] # only pinyin support`

+ Start `python scrawl.py` and enjoy! (Please comment line13 if you have already got community list)

## Database Information
```
# All communities in every region. 
class Community(BaseModel):
	id 		= PrimaryKeyField()
	title 		= CharField()
	link 		= CharField(unique=True)
	district 	= CharField()
	bizcircle 	= CharField()
	tagList 	= CharField()

# All onsale house information in every community.
class Houseinfo(BaseModel):
	houseID 	= BigIntegerField(primary_key=True)
	title 		= CharField()
	link 		= CharField()
	community 	= CharField()
	years 		= CharField()
	housetype 	= CharField()
	square 		= CharField()
	direction 	= CharField()
	floor 		= CharField()
	taxtype 	= CharField()
	totalPrice 	= IntegerField()
	unitPrice 	= IntegerField()
	followInfo 	= CharField()
	validdate 	= DateTimeField(default=datetime.datetime.now)

# All onsale house history price in every community.
class Hisprice(BaseModel):
	houseID 	= BigIntegerField()
	totalPrice 	= IntegerField()
	date 		= DateTimeField(default=datetime.datetime.now)

	class Meta:
		primary_key = CompositeKey('houseID', 'totalPrice')

# All sold house information in every community.
class Sellinfo(BaseModel):
	houseID 	= BigIntegerField(primary_key=True)
	title 		= CharField()
	link 		= CharField()
	community 	= CharField()
	years 		= CharField()
	housetype 	= CharField()
	square 		= CharField()
	direction 	= CharField()
	floor 		= CharField()
	status 		= CharField()
	source 		= CharField()
	totalPrice 	= IntegerField()
	unitPrice 	= IntegerField()
	dealdate 	= DateField()
	updatedate 	= DateTimeField(default=datetime.datetime.now)

# All rent house information in every community.
class Rentinfo(BaseModel):
	houseID 	= BigIntegerField(primary_key=True)
	title 		= CharField()
	link 		= CharField()
	region 		= CharField()
	zone 		= CharField()
	meters 		= CharField()
	other 		= CharField()
	subway 		= CharField()
	decoration 	= CharField()
	heating 	= CharField()
	price 		= IntegerField()
	pricepre 	= CharField()
	updatedate 	= DateTimeField(default=datetime.datetime.now)
```

## Examples:
![alt text](https://github.com/XuefengHuang/lianjia-scrawler/blob/master/screenshots/example1.png)
![alt text](https://github.com/XuefengHuang/lianjia-scrawler/blob/master/screenshots/example3.png)
![alt text](https://github.com/XuefengHuang/lianjia-scrawler/blob/master/screenshots/example2.png)
