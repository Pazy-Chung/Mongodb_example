from pymongo import MongoClient
import datetime
class MongoExample:
    def __init__(self, url:str)-> None:
        #initial connection setting
        self._url = url
    def pullDataFromMongoInRange(self, device_name: str, choose_collection : str, key : str,  gte, lt) -> dict:
        """Pull data from the choosen database's collection in a time interval
        Args:
            device_name(str) : To create a new database or decide which database to push data that are named by the device name.
            choose_collection(str) : There can be lots of collections in one database, we can save different type of data in different collections in same device's database.
            key(str) : Choose the key that want to compare the value.
            glt : >= this value.
            lt : < this value.
        """
        #Instance a Mongodb object and connect to Mongodb server.
        mongo_connection = MongoClient(self._url)
        #Select database.
        db = mongo_connection[device_name]
        #Select collection.
        collection = db[choose_collection]
        output= []
        #Find the target between start and end without output _id.
        for data in collection.find({key : {'$lt': lt, '$gte': gte}},{'_id': False}):
            output.append(data)
        #Disconnect Mongodb server.
        mongo_connection.close()
        #If there are no data then return -1
        if output == []:
            return -1
        else:
            return output
    def updateDataInMongo(self, device_name: str, choose_collection: str, query: dict, update_data: dict)-> None:
        """Update one key/value in database.
        Args:
            device_name(str) : To create a new database or decide which database to push data that are named by the device name.
            choose_collection(str) : There can be lots of collections in one database, we can save different type of data in different collections in same device's database.
            query : The key/value you want to update.
            update_data : The new data you want to replace into.
        """
        mongo_connection = MongoClient(self._url)
        db = mongo_connection[device_name]
        collection = db[choose_collection]
        #Set the update data we want.
        updatedata = {"$set": update_data}
        #Update to mongodb
        collection.update_one(filter = query, update = updatedata)
        mongo_connection.close()

    def pullDataWithSpecifyTarget(self, device_name: str, choose_collection : str, key:str, target) -> list:
        """Pull data that match the target.
        Args:
            device_name(str) : To create a new database or decide which database to push data that are named by the device name.
            choose_collection(str) : There can be lots of collections in one database, we can save different type of data in different collections in same device's database.
            key : Set Which key you want to find out the target.
            target : Set a target to match the value of the key.
        """
        mongo_connection = MongoClient(self._url)
        db = mongo_connection[device_name]
        collection = db[choose_collection]
        output= []
        #Below there are 2 ways to find the key/value target.
        #Aggregate and $match, this can be operate with other command.
        eventdata = collection.aggregate([
                {"$match" : {
                    key : target
                    }
                }])
        #Find, this can only be deal with 1 command.
        #eventdata = collection.find({key : target})

        for data in eventdata:
            output.append(data)
        mongo_connection.close()
        if output == []:
            return -1
        else:
            return output
    def averageDataWithSpecifyRange(self, device_name : str, choose_collection : str, key : str, gte, lt) -> dict:
        """Average the choosen key's value with a range.
        Args:
            device_name(str) : To create a new database or decide which database to push data that are named by the device name.
            choose_collection(str) : There can be lots of collections in one database, we can save different type of data in different collections in same device's database.
            key(str) : Choose the key that want to compare the value.
            glt : >= this value.
            lt : < this value.
        """
        mongo_connection = MongoClient(self._url)
        db = mongo_connection[device_name]
        collection = db[choose_collection]
        average = collection.aggregate([
            {"$match" : {
                key : {'$lt': lt, '$gte': gte}
                }
            },
            {
                "$group" : {
                    '_id': None,
                    'Average' : {'$avg' : "$" + key}
                }
            },
            {
                "$addFields" : {
                    'Round' : {'$round' : ['$Average', 1]}
                }
            }
        ])
        mongo_connection.close()
        output = []
        for data in average:
            output.append(data)
        if output == []:
            return -1
        else:
            return output

if __name__ == "__main__":
    import config
    #Connect Mongodb server.
    mongoio = MongoExample(config.mongo_ip)
    # print(mongoio.pullDataFromMongoInRange("Fruit", "Amount", "Apple", 12, 34))
    olddata = {
        "Grape" : 60
    }
    newdata = {
        "Grape" : 100
    }
    mongoio.updateDataInMongo("Fruit", "Amount", olddata, newdata)
    # print(mongoio.pullDataWithSpecifyTarget("Fruit", "Amount", 12))
    # print(mongoio.averageDataWithSpecifyRange("Fruit", "Amount", "Apple", 12, 34))
