from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import User
from accounts.models import Account
from staff.models import AccountOfficer
from accounts.helper_functions import generate_account_number
import json

# Create your views here.

@ensure_csrf_cookie
@require_GET
def home(request):
    return HttpResponse("Welcome to the myBank")

@require_POST
def create_user(request):
    data = json.loads(request.body.decode('utf-8'))
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    middle_name = data.get('middle_name', '')
    phone_number = data.get('phone_number')
    email = data.get('email')
    state_of_origin = data.get('state_of_origin')
    lga_of_origin = data.get('lga_of_origin')
    date_of_birth = data.get('date_of_birth')
    mother_maiden_name = data.get('mother_maiden_name')
    BVN = data.get('BVN')
    NIN = data.get('NIN', None)
    title = data.get('title')
    account_type = data.get('account_type')
    account_level = data.get('account_level')
    account_officer_id = data.get('MIS_CODE')

    officer = AccountOfficer.objects.filter(employee_id=account_officer_id)
    if not officer:
        return JsonResponse({'message': 'Invalid MIS Code'}, status=400)

    try:
        new_user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            phone_number=phone_number,
            email=email,
            state_of_origin=state_of_origin,
            lga_of_origin=lga_of_origin,
            date_of_birth=date_of_birth,
            mother_maiden_name=mother_maiden_name,
            BVN=BVN,
            NIN=NIN,
            title=title
        )
        new_user.save()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    account_number, account_class = generate_account_number(account_type)
    new_account = Account.objects.create(
        user=new_user,
        account_number=account_number,
        account_level=account_level,
        account_officer=officer,
        CLASS=account_class
    )
    new_account.save()
    return JsonResponse({
        'message': 'User created'}, status=201)
