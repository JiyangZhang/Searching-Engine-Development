import pymongo
from pymongo import MongoClient

"""store all the data to the database"""
def store(name, dic):  # store dictionary items in the persistent db
	client = MongoClient('mongodb://localhost:27017/')
	db = client['pagerank']
	collection = db[name]
	post_id = db[name].insert_one(dic).inserted_id

def update(name, field, value, idd):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['pagerank']
    collection = db[name]
    db[name].update_one({"id": idd},
    {"$set": {field : value}})
		
