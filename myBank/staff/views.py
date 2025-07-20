from django.http import JsonResponse
from users.models import User
from .models import AccountOfficer
from django.views.decorators.http import require_POST, require_http_methods
from django.utils import timezone
import json

# Create your views here.


@require_POST
def create_officer(request):
    data = json.loads(request.body)
    phone_number = data.get('phone_number')
    email = data.get('email')
    grade = data.get('grade')
    user_id = data.get('user_id')
    department = data.get('department')
    role = data.get('role')

    for field in ['phone_number', 'email', 'grade', 'user_id', 'department']:
        if not data.get(field):
            return JsonResponse({'error': f'{field} is required.'}, status=400)

    user = User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Validate phone number and email format if necessary
    if not phone_number.isdigit():
        return JsonResponse({'error': 'Invalid phone number format'}, status=400)

    if '@' not in email or '.' not in email.split('@')[-1]:
        return JsonResponse({'error': 'Invalid email format'}, status=400)

    try:
        officer = AccountOfficer.objects.create(
            first_name=user.first_name,
            last_name=user.last_name,
            middle_name=user.middle_name,
            phone_number=phone_number,
            official_email=email,
            department=department,
            grade=grade,
            user=user,
            role=role,
        )
        officer.save()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'Account Officer created', 'data': officer.to_dict()},
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

    return JsonResponse({'message': 'success', 'data': officer.to_dict()},
                        status=200)


@require_http_methods(["GET"])
def get_all_officers(request):
    officers = AccountOfficer.objects.all()
    officers_data = [officer.to_dict() for officer in officers]
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

    return JsonResponse({'message': 'success', 'data': officer.to_dict()},
                        status=200)
