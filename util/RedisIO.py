import redis
import json
class REDISIO:
    def __init__(self, url:str, password:str) -> None:
        # set connection parameters
        self._connection_pool = redis.ConnectionPool.from_url(url= url, password = password)
    def pushDataToRedis(self, key: str, data: dict) -> None:
        """Push data to redis server.
            Work with pullDataFromRedis().
        Args:
            key (str): redis key to push data into.
            data (dict): data to push to redis server.
        """
        # Instance an redis object and connect to redis server.
        redis_connection = redis.Redis(connection_pool = self._connection_pool)
        # Change dictionary to json.
        value = json.dumps(data)
        # Push value on redis.
        redis_connection.set(key, value)
        # Disconnect redis server.
        redis_connection.close()
    def pullDataFromRedis(self, key: str) -> dict:
        """Fetch data from redis server.
            Work with pushDataToRedis().
        Args:
            key (str): key to fetch data with.

        Returns:
            dict: data from redis server
        """
        # Instance an redis object and connect to redis server.
        redis_connection = redis.Redis(connection_pool = self._connection_pool)
        # Pull data from redis with key
        value = redis_connection.get(key)
        # Change Json into dictionary.
        output = json.loads(value.decode('utf-8'))
        # Disconnect redis server.
        redis_connection.close()
        return output 
    def popList(self, key:str) -> dict:
        """PoP data from redis list.
            Work with pushList().
        Args:
            key (str): key to pop data from redis server.

        Returns:
            dict: value from redis server
        """
        # Instance an redis object and connect to redis server.
        redis_connection = redis.Redis(connection_pool = self._connection_pool)
        # POP 1 object in "key" db.
        value = redis_connection.lpop(key, 1)
        if value is None:
            return None
        # Disconnect redis server.
        redis_connection.close()
        # Change Json into dictionary.
        value = json.loads(value[0].decode('utf-8'))
        return value
    def pushList(self, key:str, data:dict) -> None:
        """Push data into redis list.
            Work with popList().
        Args:
            key (str): key to push data into redis.
            data (dict): value to push on redis.
        """
        # Instance an redis object and connect to redis server.
        redis_connection = redis.Redis(connection_pool = self._connection_pool)
        # Change dictionary to json.
        value = json.dumps(data)
        # Change dictionary to json.
        redis_connection.rpush(key, value)
        # Disconnect redis server.
        redis_connection.close()
        
if __name__ == "__main__":
    import config
    # Try to connect redis server
    redisIO = REDISIO(config.redis_ip, config.redis_password)
    # Print key:"15KW" Value
    print(redisIO.pullDataFromRedis('15KW'))
