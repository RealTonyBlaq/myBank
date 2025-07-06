from django.http import JsonResponse
from .models import AccountOfficer
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST, require_http_methods
from django.utils import timezone
import json

# Create your views here.


@require_POST
def create_officer(request):
    data = json.loads(request.body)
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    middle_name = data.get('middle_name', '')
    phone_number = data.get('phone_number')
    email = data.get('email')
    grade = data.get('grade')
    if not first_name or not last_name or not phone_number or not email:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    # Validate phone number and email format if necessary
    if not phone_number.isdigit():
        return JsonResponse({'error': 'Invalid phone number format'}, status=400)

    if '@' not in email or '.' not in email.split('@')[-1]:
        return JsonResponse({'error': 'Invalid email format'}, status=400)

    # Default department to 'Sales' if not provided
    department = data.get('department', 'Sales')

    try:
        officer = AccountOfficer.objects.create(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            phone_number=phone_number,
            official_email=email,
            department=department,
            grade=grade
        )
        officer.save()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'success', 'data': model_to_dict(officer)},
                        status=201)


@require_http_methods(["DELETE"])
def delete_officer(request, officer_id):
    officer = AccountOfficer.objects.filter(employee_id=officer_id).first()
    if not officer:
        return JsonResponse({'error': 'Officer not found'}, status=404)

    officer.delete()
    return JsonResponse({'message': 'Officer deleted successfully'},
                        status=204)


@require_http_methods(["GET"])
def get_officer(request, officer_id):
    officer = AccountOfficer.objects.filter(employee_id=officer_id).first()
    if not officer:
        return JsonResponse({'error': 'Officer not found'}, status=404)

    return JsonResponse({'message': 'success', 'data': model_to_dict(officer)},
                        status=200)


@require_http_methods(["GET"])
def get_all_officers(request):
    officers = AccountOfficer.objects.all()
    officers_data = [model_to_dict(officer) for officer in officers]
    return JsonResponse({'message': 'success', 'data': officers_data}, status=200)


@require_http_methods(['PATCH'])
def update_officer(request, officer_id):
    data = json.loads(request.body)
    officer = AccountOfficer.objects.filter(employee_id=officer_id).first()
    if not officer:
        return JsonResponse({'error': 'Officer not found'}, status=404)

    try:
        for key, value in data.items():
            if key not in ['employee_id', 'created_at', 'updated_at']:
                setattr(officer, key, value)
        officer.updated_at = timezone.now()
        officer.save()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'success', 'data': model_to_dict(officer)},
                        status=200)
