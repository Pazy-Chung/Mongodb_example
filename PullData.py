from datetime import datetime, timedelta
from util.OtherMongoCommandExample import MongoExample
import util.config as config
import time
#5 mins ago -> datetime
fivemin = datetime.now() + timedelta(minutes= -10)
#Transfer into timestamp
fiveminsago = int(round(fivemin.timestamp()))
print("Integer timestamp of current datetime: ", fiveminsago)
#Timestamp now
now = int(time.time())
print("time.time", int(time.time()))
#Connect Mongodb server.
mongoio = MongoExample(config.mongo_ip)
#Pull the data in a specify time interval from database name : "example_device_1" and collection name : "data" and print.
print(mongoio.pullDataFromMongoInRange("example_device_1", "data", "CreatAt", fiveminsago, int(time.time())))
