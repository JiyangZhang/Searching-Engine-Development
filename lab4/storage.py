"""last update 12.01  20:56"""

import pymongo
from pymongo import MongoClient

"""store all the data to the database"""
def store(name, dic):  # store dictionary items in the persistent db
	client = MongoClient('mongodb://localhost:27017/')
	db = client['eecgdata']
	collection = db[name]
	post_id = db[name].insert_one(dic).inserted_id

def update(name, field, value, idd):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['eecgdata']
    collection = db[name]
    db[name].update_one({"id": idd},
    {"$set": {field : value}})
		
def find_one(doc_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['eecgdata']
    posts = db['documet_index']
    document = dict(posts.find_one({"id": doc_id}))
    return document['img'] # return a list of img_url