import mongoengine
import src.utils.db_utils as db_utils


def delete_user(schema: mongoengine.Document, chat_id: str) -> str:
    try:
        if not db_utils.check_account_exist(schema, chat_id) or not schema.objects(chat_id=chat_id):
            raise mongoengine.DoesNotExist(f'No such account: {chat_id}')
        target = schema.objects(chat_id=chat_id)
        target.delete()
        return f'{chat_id} removed'
    except mongoengine.DoesNotExist as e:
        return f'{e}'
    except Exception as e:
        return f'{e}'
