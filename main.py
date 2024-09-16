from util.RedisIO import REDISIO
from util.MongoIO import MONGOIO
import util.config as config
import time
def main():
    #Connect Mongodb server.
    mongoio = MONGOIO('mongodb://ncu:qwert123456@localhost:27017/')
    #Connect Redis server.
    redisIO = REDISIO(config.redis_ip, config.redis_password)
    while True :
        #Pull data from redis.
        datafromredis = redisIO.pullDataFromRedis("example_device_1")
        #Save the data from redis into Mongodb where the database name is "example_device_1" and collection name is "data".
        datafromredis["CreatAt"] = int(time.time())
        mongoio.pushDataToMongo("example_device_1", "data", datafromredis)
        #Pull the data from database name : "example_device_1" and collection name : "data" and print.
        print(mongoio.pullDataFromMongo("example_device_1", "data"))
        time.sleep(10)
if __name__ == '__main__':
    main()    
