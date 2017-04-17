from peewee import *
import datetime
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

if config.getboolean('Mysql', 'enable'):
	database = MySQLDatabase(
		config.get('Mysql', 'scheme'),
		host=config.get('Mysql', 'host'),
		port=config.getint('Mysql', 'port'),
		user=config.get('Mysql', 'user'),
		passwd=config.get('Mysql', 'password'),
		charset='utf8',
		use_unicode=True,
	)

elif config.getboolean('Sqlite', 'enable'):
	database = SqliteDatabase(config.get('Sqlite', 'dbname'))

elif config.getboolean('Postgresql', 'enable'):
	database = PostgresqlDatabase(
		config.get('Postgresql', 'scheme'),
		user=config.get('Postgresql', 'user'),
		password=config.get('Postgresql', 'password'),
		host=config.get('Postgresql', 'host'),
		charset='utf8',
		use_unicode=True,
	)

else:
	raise AttributeError("Please enable a datatbase at config.ini")

class BaseModel(Model):
    class Meta:
        database = database

class Community(BaseModel):
	id 		= PrimaryKeyField()
	title 		= CharField()
	link 		= CharField(unique=True)
	district 	= CharField()
	bizcircle 	= CharField()
	tagList 	= CharField()

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

class Hisprice(BaseModel):
	houseID 	= BigIntegerField()
	totalPrice 	= IntegerField()
	date 		= DateTimeField(default=datetime.datetime.now)

	class Meta:
		primary_key = CompositeKey('houseID', 'totalPrice')

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

def database_init():
    database.connect()
    database.create_tables([Community, Houseinfo, Hisprice, Sellinfo, Rentinfo], safe=True)
    database.close()
