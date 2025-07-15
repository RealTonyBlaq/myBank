import random
from utilities.defaults import get_account_defaults, set_account_defaults


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

    set_account_defaults() # Ensure defaults are set before generating account number
    if not account_type:
        raise ValueError("Account type must be specified.")

    try:
        ACCOUNT_DEFAULTS = get_account_defaults(account_type)
    except ValueError:
        raise ValueError(f"No defaults found for account type: {account_type}")

    prefix = ACCOUNT_DEFAULTS.get('PREFIX')
    while True:
        suffix = ''.join(random.choices('0123456789', k=7))
        account_number = f"{prefix}{suffix}"
        if not Account.objects.filter(account_number=account_number).exists():
            return account_number, ACCOUNT_DEFAULTS
