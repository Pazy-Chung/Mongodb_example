from pymongo import MongoClient
class MONGOIO:
    def __init__(self, url:str)-> None:
        #initial connection setting
        self._url = url
    def pushDataToMongo(self, device_name: str, choose_collection: str, data: dict) -> None:
        """Push data to the choosen database's collection in Mongodb server.
        Args:
            device_name(str) : To create a new database or decide which database to push data that are named by the device name.
            choose_collection(str) : There can be lots of collections in one database, we can save different type of data in different collections in same device's database.
            data (dict) : data to push into Mongodb. 
        """
        #Instance a Mongodb object and connect to Mongodb server.
        mongo_connection = MongoClient(self._url)
        #Select database.
        db = mongo_connection[device_name]
        #Select collection.
        collection = db[choose_collection]
        #push data to the choosen collection.
        collection.insert_one(data)
        #Disconnect Mongodb server.
        mongo_connection.close()
    def pullDataFromMongo(self, device_name: str, choose_collection : str) -> list:
        """Pull data from the choosen database's collection in a time interval
        Args:
            device_name(str) : To create a new database or decide which database to push data that are named by the device name.
            choose_collection(str) : There can be lots of collections in one database, we can save different type of data in different collections in same device's database.
            start(datetime) :The beginning of the time interval.
            end(datetime) : The end of the time interval
        """
        #Instance a Mongodb object and connect to Mongodb server.
        mongo_connection = MongoClient(self._url)
        #Select database.
        db = mongo_connection[device_name]
        #Select collection.
        collection = db[choose_collection]
        output= []
        for data in collection.find():
            output.append(data)
        mongo_connection.close()
        if output == []:
            return -1
        else:
            return output
if __name__ == "__main__":
    import config
    #Connect Mongodb server.
    mongoio = MONGOIO(config.mongo_ip)
    example = {
        "Apple" : 34,
        "Banana" : 15,
        "Grape" : 60
    }
    #Save example(dict) into Mongodb where the database name is "Fruit" and collection name is "Amount".
    mongoio.pushDataToMongo("Fruit", "Amount", example)
    #Pull the data from database name : "Fruit" and collection name : "Amount" and print.
    print(mongoio.pullDataFromMongo("Fruit", "Amount"))


    