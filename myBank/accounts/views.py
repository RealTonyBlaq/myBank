from users.models import User
from staff.models import AccountOfficer
from .models import Account
from .helper_functions import generate_account_number
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
import json


# Create your views here.
@require_GET
def info(request, account_number):
    """ Returns all the information on an account """
    try:
        account = Account.objects.get(account_number=account_number)
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)

    return JsonResponse(account.to_dict(), status=200)


@require_POST
def create_account(request):
    """ Endpoint to create a new account """
    data = json.loads(request.body.decode('utf-8'))
    user_id = data.get('user_id')
    account_officer_id = data.get('account_officer_id')
    account_level = data.get('account_level')
    account_type = data.get('account_type')

    for field in ['user_id', 'account_officer_id', 'account_level', 'account_type']:
        if not data.get(field):
            return JsonResponse({'error': f'{field} is required.'}, status=400)

    user = User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Check if user qualifies for the account level
    # Check if user has accounts

    account_officer = AccountOfficer.objects.filter(employee_id=account_officer_id).first()
    if not account_officer:
        return JsonResponse({'error': 'Account Officer not found'}, status=404)

    try:
        account_number, account_defaults = generate_account_number(account_type)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    try:
        account = Account.objects.create(
            user=user,
            account_officer=account_officer,
            account_number=account_number,
            account_level=account_level,
            CLASS=account_defaults
        )
        account.save()
        return JsonResponse({'message': 'Account created',
                             'data': account.to_dict()}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
