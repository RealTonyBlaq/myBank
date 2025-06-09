from django.http import JsonResponse
from .models import AccountOfficer
from django.views.decorators.http import require_POST
import json

# Create your views here.

@require_POST
def create_officer(request):
    data = json.loads(request.body.encode('utf-8'))
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    middle_name = data.get('middle_name', '')
    phone_number = data.get('phone_number')
    email = data.get('official_name')
    department = data.get('department', 'Sales')

    try:
        officer = AccountOfficer.objects.create(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            phone_number=phone_number,
            official_email=email,
            department=department
        )
        officer.save()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'success', 'data': officer.__dict__}, status=201)
