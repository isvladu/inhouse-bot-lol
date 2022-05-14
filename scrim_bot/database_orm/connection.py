import pymongo
from config import DB_TOKEN


class Connection:
    """
    A class that initializes the connection to the database and has all the required operations.
    """

    def __init__(self):
        self.client = pymongo.MongoClient(DB_TOKEN)
        self.database = self.client["scrimbot"]

    def getCollection(self, collection_name: str):
        return self.database[collection_name]
