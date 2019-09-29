import mongoengine


def check_account_exist(model: mongoengine.Document, chat_id) -> bool:
    try:
        return bool(model.objects(chat_id=str(chat_id)))
    except Exception as e:
        print(e)
        return False
