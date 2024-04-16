
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://<username>:<password>@npmapi.cwcmktm.mongodb.net/?retryWrites=true&w=majority&appName=<cluster>"

# Create a new client and connect to the server
client = MongoClient(uri)

db = client.todolist_db
collection = db["todolist"]