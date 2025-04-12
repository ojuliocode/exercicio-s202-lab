
import os
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# arquivo baseado nas aulas anteriores
class Database:
    def __init__(self, database_name="uber_teste", collection_name="Motoristas"):
        USER = "mongo"
        PASSWORD = "mongo"
        HOST = "localhost"
        PORT = 27017
        DB_NAME = database_name
        COLLECTION_NAME = collection_name
        uri = f"mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}/?authSource=admin" 
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def get_collection(self):
        return self.collection

    def close(self):
        if hasattr(self, 'client'):
            self.client.close()