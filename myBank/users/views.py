from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import User
import json

# Create your views here.

@ensure_csrf_cookie
@require_GET
def home(request):
    return HttpResponse("Welcome to myBank")

@require_POST
def create_user(request):
    """ Create a new user with the provided details.
    The request body should contain the following fields:
    - first_name
    - last_name
    - middle_name (optional)
    - phone_number
    - email
    - state_of_origin
    - lga_of_origin
    - date_of_birth (format: YYYY-MM-DD)
    - mother_maiden_name
    - BVN (optional, but either BVN or NIN must be provided)
    - NIN (optional, but either BVN or NIN must be provided)
    - title
    """
    data = json.loads(request.body.decode('utf-8'))
    BVN = data.get('BVN')
    NIN = data.get('NIN')

    if not BVN and not NIN:
        return JsonResponse({'error': 'Either BVN or NIN must be provided'}, status=400)

    existing_user = User.objects.filter(BVN=BVN, NIN=NIN).first()
    if existing_user:
        return JsonResponse({'error': 'User exists', 'existing_user_id': existing_user.id}, status=400)

    for field in ['first_name', 'last_name', 'phone_number',
                  'email', 'state_of_origin', 'lga_of_origin',
                  'date_of_birth', 'mother_maiden_name', 'title']:
        if not data.get(field):
            return JsonResponse({'error': f'{field} is required.'}, status=400)

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    middle_name = data.get('middle_name', '')
    phone_number = data.get('phone_number')
    email = data.get('email')
    state_of_origin = data.get('state_of_origin')
    lga_of_origin = data.get('lga_of_origin')
    date_of_birth = data.get('date_of_birth')
    mother_maiden_name = data.get('mother_maiden_name')
    title = data.get('title')

    try:
        formatted_date = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
    except Exception:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    try:
        new_user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            phone_number=phone_number,
            email=email,
            state_of_origin=state_of_origin,
            lga_of_origin=lga_of_origin,
            date_of_birth=formatted_date,
            mother_maiden_name=mother_maiden_name,
            BVN=BVN,
            NIN=NIN,
            title=title
        )
        new_user.save()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({
        'message': 'User created', 'data': new_user.to_dict()}, status=201)


@require_http_methods(["PUT"])
def update_user(request, user_id):
    """ Update an existing user with the provided details.
    The request body should contain the fields to be updated.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    data = json.loads(request.body.decode('utf-8'))
    for field in ['first_name', 'last_name', 'middle_name', 'phone_number',
                  'email', 'state_of_origin', 'lga_of_origin', 'date_of_birth',
                  'mother_maiden_name', 'BVN', 'NIN', 'title']:
        if field in data:
            setattr(user, field, data[field])

    user.date_updated = datetime.now()
    user.save()
    return JsonResponse({'message': 'User updated successfully', 'data': user.to_dict()},
                        status=200)

@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    """ Delete a user by ID. """
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@require_GET
def get_user(request, user_id):
    """ Retrieve a user by ID. """
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({'data': user.to_dict()}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@require_GET
def list_users(request):
    """ List all users. """
    users = User.objects.all()
    user_list = [user.to_dict() for user in users]
    return JsonResponse({'data': user_list}, status=200)
