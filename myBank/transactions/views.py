from accounts.models import Account
from transactions.models import Credit, Debit, Ledger
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

# Create your views here.

@require_POST
def inflow(request):
    """ Receives inflows into an account. """
    data = json.loads(request.body)
    account_number = data.get('account_number')
    amount = float(data.get('amount'))
    description = data.get('description', '')
    sender_name = data.get('sender_name')
    sender_bank = data.get('sender_bank')
    sender_account_number = data.get('sender_account_number')
    session_id = data.get('session_id')
    transaction_type = data.get('transaction_type', 'transfer')

    for field in ['account_number', 'amount', 'sender_name', 'sender_bank', 'sender_account_number', 'session_id']:
        if not data.get(field):
            return JsonResponse({'error': f'{field} is required.'}, status=400)

    account = Account.objects.filter(account_number=account_number).first()

    if not account:
        return JsonResponse({'error': 'Account number not found.'}, status=404)

    # Check account level

    # Credit account with value
    new_credit = Credit(account=account,
                        amount=amount,
                        session_id=session_id,
                        narration=description,
                        transaction_type=transaction_type)
    new_credit.save()

    # Ledger
    new_ledger = Ledger(transaction_id=new_credit.transaction_id,
                        status=new_credit.status,
                        account=account,
                        entry_type='debit',
                        amount=amount,
                        narration=f'[{sender_account_number}/{sender_bank}] \
                            {sender_name} sent {amount} - NARRATION [{description}]')
    new_ledger.save()

    # Post credit actions:
    # 1. Check account level and place PND if necessary
    # 2. Send notification - SMS & Email

    return JsonResponse({'message': 'successful'}, status=201)
