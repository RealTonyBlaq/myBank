import random


ACCOUNT_DEFAULTS = {
    'SAVINGS': {
        'PREFIX': '400',
        'ACC_CODE': 'CUSACC',
        'ACC_TYPE': 'SAVINGS',
        'ACC_DETAIL': 'INDIVIDUAL SAVINGS ACCOUNT'
    },
    'CURRENT': {
        'PREFIX': '410',
        'ACC_CODE': 'CUCACC',
        'ACC_TYPE': 'CURRENT',
        'ACC_DETAIL': 'INDIVIDUAL CURRENT ACCOUNT'
    },
    'FIXED': {
        'PREFIX': '411',
        'ACC_CODE': 'CUFACC',
        'ACC_TYPE': 'FIXED',
        'ACC_DETAIL': 'INDIVIDUAL FIXED DEPOSIT ACCOUNT'
    }
}


def calculate_account_balance(account) -> float:
    """
    Calculate the balance of a given account.
    
    Args:
        account: The account for which to calculate the balance.
    
    Returns:
        float: The calculated balance of the account.
    """
    if not account:
        return 0.0

    # if account.account_type.lower() in ['savings', 'current']:
    total_debits = sum([value for value.amount in account.debits.all()]) # type: ignore
    total_credits = sum([value for value.amount in account.credits.all()]) # type: ignore 
    balance = total_credits - total_debits
    return balance
    # return 0.0

def generate_account_number(account_type: str) -> tuple[str, dict]:
    """
    Generate a unique account number.
    
    Returns:
        str: A unique account number.
    """
    from .models import Account
    prefix = ACCOUNT_DEFAULTS.get(account_type.upper(), {}).get('PREFIX', '400') # default to SAVINGS prefix if not found
    while True:
        suffix = ''.join(random.choices('0123456789', k=7))
        account_number = f"{prefix}{suffix}"
        if not Account.objects.filter(account_number=account_number).exists():
            return account_number, ACCOUNT_DEFAULTS.get(account_type.upper(), ACCOUNT_DEFAULTS['SAVINGS'])
