import mongoengine

client = mongoengine.connect('MUP_User')
print(f'Mongo is connected at  {client.HOST} : {client.PORT}')


class User(mongoengine.Document):
    chat_id = mongoengine.StringField(required=True)
    account = mongoengine.StringField(required=True)
