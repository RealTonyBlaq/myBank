from utilities.database import db
from typing import List, Dict


def set_account_defaults(data: List[Dict] = []):
    """
    Sets a new default for accounts

    Parameter:

    Data: List of Dictionaries

    Each Dictionary must have a 'type' and 'value' key

    type - The type of account

    value - The defaults to be set.
            keys: PREFIX, ACC_CODE, ACC_TYPE, ACC_DETAIL
    """

    ACCOUNT_DEFAULTS = [
        {
            'type': 'SAVINGS',
            'value': {
                'PREFIX': '400',
                'ACC_CODE': 'CUSACC',
                'ACC_TYPE': 'SAVINGS',
                'ACC_DETAIL': 'INDIVIDUAL SAVINGS ACCOUNT'
            }
        },
        {
            'type': 'CURRENT',
            'value': {
                'PREFIX': '410',
                'ACC_CODE': 'CUCACC',
                'ACC_TYPE': 'CURRENT',
                'ACC_DETAIL': 'INDIVIDUAL CURRENT ACCOUNT'
            }
        },
        {
            'type': 'FIXED',
            'value': {
                'PREFIX': '411',
                'ACC_CODE': 'CUFACC',
                'ACC_TYPE': 'FIXED DEPOSIT',
                'ACC_DETAIL': 'INDIVIDUAL FIXED DEPOSIT ACCOUNT'
            }
        }
    ]

    collection_name = 'defaults'
    inserted_count = 0

    for acc in ACCOUNT_DEFAULTS + data:
        if not db.doc_exists(collection_name, {'type': acc['type']}):
            inserted_count += len(db.insert_documents(collection_name, [acc]))

    print(f"Inserted {inserted_count} account defaults into the database.")


def get_account_defaults(account_type: str) -> dict:
    """ Retrieves the default values for a given account type. """
    collection_name = 'defaults'
    query = {'type': account_type.upper()}
    defaults = db.find_documents(collection_name, query)

    if defaults != []:
        return defaults[0]['value']
    else:
        raise ValueError(f"No defaults found for account type: {account_type}")


def get_all_account_defaults() -> List[Dict]:
    """ Retrieves all account defaults. """
    collection_name = 'defaults'
    return db.find_documents(collection_name)
