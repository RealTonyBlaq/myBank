from datetime import datetime
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from users.models import User, NextOfKin


@require_GET
def get_nok(request, user_id):
    """ Retrieve the next of kin details for a user by user ID. """
    try:
        user = User.objects.get(id=user_id)
        next_of_kin = user.next_of_kin  # type: ignore
        if not next_of_kin.exists():
            return JsonResponse({'error': 'Next of kin not found'}, status=404)
        return JsonResponse(next_of_kin.to_dict(), status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


@require_POST
def create_nok(request, user_id):
    """ Create a new next of kin for a user. """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    data = json.loads(request.body.decode('utf-8'))
    required_fields = ['first_name', 'last_name', 'relationship', 'phone_number']

    for field in required_fields:
        if field not in data:
            return JsonResponse({'error': f'{field} is required.'}, status=400)

    next_of_kin = NextOfKin.objects.create(
        user=user,
        first_name=data['first_name'],
        last_name=data['last_name'],
        middle_name=data.get('middle_name', ''),
        email=data.get('email', ''),
        address=data.get('address', ''),
        relationship=data['relationship'],
        phone_number=data['phone_number'],
        state=data.get('state', ''),
        lga=data.get('lga', '')
    )
    next_of_kin.save()

    return JsonResponse({'message': 'Next of kin created successfully', 'data': next_of_kin.to_dict()}, status=201)


@require_http_methods(["PUT"])
def update_nok(request, user_id):
    """ Update an existing next of kin for a user. """
    try:
        user = User.objects.get(id=user_id)
        next_of_kin = user.next_of_kin  # type: ignore
        if not next_of_kin.exists():
            return JsonResponse({'error': 'Next of kin not found'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    data = json.loads(request.body.decode('utf-8'))
    for field in ['first_name', 'last_name', 'middle_name', 'phone_number',
                  'email', 'relationship', 'address', 'state', 'lga']:
        if field in data:
            setattr(next_of_kin, field, data[field])

    next_of_kin.updated_at = datetime.now()
    next_of_kin.save()
    return JsonResponse({'message': 'Next of kin updated successfully', 'data': next_of_kin.to_dict()},
                        status=200)


@require_http_methods(["DELETE"])
def delete_nok(request, user_id):
    """ Delete the next of kin for a user by user ID. """
    try:
        user = User.objects.get(id=user_id)
        next_of_kin = user.next_of_kin  # type: ignore
        if not next_of_kin.exists():
            return JsonResponse({'error': 'Next of kin not found'}, status=404)
        next_of_kin.delete()
        return JsonResponse({'message': 'Next of kin deleted successfully'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
