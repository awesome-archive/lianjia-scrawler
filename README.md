# lianjia-scrawler
This repo provides a tool to scrawl house info at LianJia.com. The data will be stored in Mysql datatbase. It will be easy to export to CSV or other formates. You also can [sync Mysql to Elasticsearch](https://github.com/siddontang/go-mysql-elasticsearch). In this way, you can use [kibana](https://github.com/elastic/kibana) to analyse these data.

This tool could collect cellname from each region at first, then you'd like to use these cellnames to learn about onsale, history price, sold and rent information.

## Usage
```
git clone https://github.com/XuefengHuang/lianjia-scrawler.git
cd lianjia-scrawler
virtualenv lianjia
source lianjia/bin/activate
pip install -r requirements.txt
# Modify database config in model.py at this part: database = MySQLDatabase("SCHEME", host="YOUR_MYSQL_HOST", port=3306, user="USERNAME", passwd="PASSWORD")
# Example: database = MySQLDatabase("lianjia", host="127.0.0.1", port=3306, user="root", passwd="123456")
python scrawl.py
```

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
