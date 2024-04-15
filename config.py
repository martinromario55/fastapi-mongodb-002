
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://martinromario55:JXygJtD2XcG5ZQYy@npmapi.cwcmktm.mongodb.net/?retryWrites=true&w=majority&appName=NPMAPI"

# Create a new client and connect to the server
client = MongoClient(uri)

db = client.todolist_db
collection = db["todolist"]