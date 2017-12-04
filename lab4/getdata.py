"""author : Jiyang Zhang
   last update : 12.1  20:39
"""

import pymongo
from pymongo import MongoClient

# get the word's id 
def word_to_id(word):
	client = MongoClient('mongodb://localhost:27017/')
	db = client['eecgdata']
	posts = db['lexicon']
	if posts.find_one({"word": word}) == None:
		return "wrong"
	document = dict(posts.find_one({"word": word}))
	return document['id']
	
# from word_id get doc_id
def word_to_doc(word_id):
	if word_id == "wrong":
		return "wrong"
	client = MongoClient('mongodb://localhost:27017/')
	db = client['eecgdata']
	posts = db['inverted_index']
	document = dict(posts.find_one({"words_id": word_id}))
	return document['doc_id']  # return a list


def rank(l):  # return list of tuples, (doc_id, score)
	if l == "wrong":
		return "wrong"
	score_dic = {}
	client = MongoClient('mongodb://localhost:27017/')
	db = client['eecgdata']
	posts = db['page_rank']
	for i in l:
		if posts.find_one({"doc_id": i}) == None:
			score_dic[i] = 10000
		else:
			document = dict(posts.find_one({"doc_id": i}))
			score_dic[i] = document['score']
	sorted_l = sorted(score_dic.items(), key = lambda item :item[1])
	sorted_l = sorted_l[::-1]
	return sorted_l

# a list of tuples
def sorted_url(sorted_l):
	if sorted_l == "wrong":
		return "wrong"
	client = MongoClient('mongodb://localhost:27017/')
	db = client['eecgdata']
	posts = db['documet_index']
	l = []
	for i, j in sorted_l:
		if posts.find_one({"id" : i}) == None:
			pass
		else:
			document = dict(posts.find_one({"id" : i}))
			l.append(document['url'])
	return l

def img_url(sorted_l):
	if sorted_l == "wrong":
		return "wrong"
	client = MongoClient('mongodb://localhost:27017/')
    	db = client['eecgdata']
    	posts = db['documet_index']
    	l = []
    	for i, j in sorted_l:
        	if posts.find_one({"id": i}) == None:
            		pass
        	else:
            		document = dict(posts.find_one({"id": i}))
	    		if len(document['img']):
				for item in document['img']:
					l.append(item)
    	return l


def word_to_urls(word):
	number = word_to_id(word)  # return the id of word
	doc_list = word_to_doc(number) # return the doc_list of a word
	sorted_list = rank(doc_list)  # return a sorted list of tuples (doc_id, score)
	url_list = sorted_url(sorted_list)  # return a list of sorted url list
	return url_list

def word_to_img(word):
	number = word_to_id(word)  # return the id of word
    	doc_list = word_to_doc(number)  # return the doc_list of a word
    	sorted_list = rank(doc_list)  # return a sorted list of tuples (doc_id, score)
    	url_list = img_url(sorted_list)  # return a list of sorted url list
    	return url_list
 
