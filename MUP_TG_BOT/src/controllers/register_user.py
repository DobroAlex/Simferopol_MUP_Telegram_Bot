import mongoengine
import src.utils.page_parsing as page_parsing
import src.utils.link_generator as link_gen
import src.utils.db_utils as db_utils


def register_user(schema: mongoengine.Document, account_id: object, chat_id: object) -> object:
    try:
        page_to_check = link_gen.generate_page_from_account(account_id)
        if not page_parsing.is_valid_page(page_to_check):
            raise RuntimeError(f'{page_to_check} for account {account_id} doesn\'t exist --> invalid account')
        if db_utils.check_account_exist(schema, chat_id):
            raise mongoengine.NotUniqueError(f'{chat_id} already exists')
        schema(chat_id=chat_id, account=account_id).save()
        return f'New user {str(chat_id)} : {account_id} saved'
    except (RuntimeError, mongoengine.NotUniqueError) as e:
        return f'{e}'
    except Exception as e:  # Handling everything else
        return f'{e}'
