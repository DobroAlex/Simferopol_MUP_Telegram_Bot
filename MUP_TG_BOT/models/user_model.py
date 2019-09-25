import pymongo

client = pymongo.MongoClient()
print(f'Mongo is connected at  {client.address}')
db = client.MUP_Users
collection = db.MUP_Users


