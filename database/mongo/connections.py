from pymongo import MongoClient
from fastapi import Depends


DATABASE_NAME = "profile"


# Mongodb configuration
def get_mongodb():
    client = MongoClient()
    database = client.profile
    return database
