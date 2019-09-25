import pymongo

client = pymongo.MongoClient()
print(f'Mongo is connected at  {client.address}')
db = client.MUP_User
collection = db.MUP_User


