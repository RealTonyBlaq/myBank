import random
from utilities.defaults import get_account_defaults, set_account_defaults


def calculate_account_balance(account) -> str:
    """
    Calculate the balance of a given account.
    
    Args:
        account: The account for which to calculate the balance.
    
    Returns:
        float: The calculated balance of the account.
    """
    if not account:
        return '0.00'

    # if account.account_type.lower() in ['savings', 'current']:
    total_debits = sum([value.amount for value in account.debits.all()]) if account.debits.exists() else 0.00
    total_credits = sum([value.amount for value in account.credits.all()]) if account.credits.exists() else 0.00
    balance = total_credits - total_debits
    return f'{balance:,.2f}'


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
