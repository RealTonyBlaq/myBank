from django.shortcuts import render
from accounts.models import Account
from .models import Debit
from ledgers.models import Ledger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from dotenv import load_dotenv, find_dotenv
import json
import os

# Create your views here.

load_dotenv(find_dotenv())
TIER_ONE_INFLOW_LIMIT = float(os.getenv('TIER_ONE_INFLOW_LIMIT', 50000))
TIER_ONE_MAX_BALANCE = float(os.getenv('TIER_ONE_MAX_BALANCE', 300000))
TIER_ONE_OUTFLOW_LIMIT = float(os.getenv('TIER_ONE_OUTFLOW_LIMIT', 20000))


@require_POST
def outflow(request):
    """ Creates a debit transaction from an account """
    data = json.loads(request.body)
    beneficiary_account_number = data.get('beneficiary_account_number')
    beneficiary_bank = data.get('beneficiary_bank')
    beneficiary_bank_api_url = data.get('beneficiary_bank_api_url')
    beneficiary_name = data.get('beneficiary_name')
    account_number = data.get('account_number')
    amount = float(data.get('amount'))
    narration = data.get('narration')
    transaction_type = data.get('transaction_type', 'outward_transfer')

    for field in ['beneficiary_account_number', 'beneficiary_bank', 'beneficiary_name',
                  'account_number', 'amount', 'narration']:
        if not data.get(field):
            return JsonResponse({'error': f'{field} is required.'}, status=400)

    account = Account.objects.filter(account_number=account_number).first()
    if not account:
        return JsonResponse({'error': 'Account number not found.'}, status=404)

    if account.balance < amount:
        return JsonResponse({'error': 'Insufficient funds'}, status=400)

    # 1. Check account level
    # 2. Check transfer limits
    # 3. Check if daily outflow limit has been reached

    if account.account_level == '1' and amount > TIER_ONE_OUTFLOW_LIMIT:
        return JsonResponse({'error': f'Transfer limit exceeded for account level'}, status=400)
