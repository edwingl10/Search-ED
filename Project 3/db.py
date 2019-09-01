'''
this entire file is used to store and retrieve information regarding the 
inverted index within the database 
'''


from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017) # Local Database Connection
db = client['index'] # Connecting Database
tokenCollection = db['words'] # Connecting to Collection AKA Table

#inserts inverted index to database
def insert(index_dict):
    for k, v in index_dict.items():
        tokenCollection.insert_one( {'word' : k, 'info' : v})

#prints content of database
def print_db():
    cursor = tokenCollection.find({})
    for doc in cursor:
        print(doc)
        
#clears the entire database     
def remove():
    return tokenCollection.drop()

#finds the query 
def find(user_query):
    return tokenCollection.find_one({'word': user_query})
    

