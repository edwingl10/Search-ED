'''
This file is used to store the url associated with the folder_name/file_name
It stores this information in a database using mongodb
'''

from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017) # Local Database Connection
db = client['index'] # Connecting Database
tokenCollection = db['pageURL'] # Connecting to Collection AKA Table

#inserts folder/file name with its URL as its value
def insert(url_dict):
    for k, v in url_dict.items():
        tokenCollection.insert_one( {'name' : k, 'URL' : v})
        
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
    return tokenCollection.find_one({'name': user_query})



    