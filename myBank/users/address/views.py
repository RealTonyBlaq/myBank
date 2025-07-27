from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from users.models import User, Address
import json


@require_GET
def get_address(request, user_id):
    """ Retrieve the address of a user by user ID. """
    try:
        user = User.objects.get(id=user_id)
        address = user.address # type: ignore
        if not address.exists():
            return JsonResponse({'error': 'Address not found'}, status=404)
        return JsonResponse(address.to_dict(), status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@require_POST
def create_address(request, user_id):
    """ Create a new address for a user. """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    data = json.loads(request.body.decode('utf-8'))
    required_fields = ['city', 'state', 'local_government_area', 'nearest_bus_stop',
                       'house_number', 'street_name', 'postal_code']

    for field in required_fields:
        if field not in data:
            return JsonResponse({'error': f'{field} is required.'}, status=400)

    address = Address.objects.create(
        user=user,
        city=data['city'],
        state=data['state'],
        local_government_area=data['local_government_area'],
        nearest_bus_stop=data['nearest_bus_stop'],
        house_number=data['house_number'],
        street_name=data.get('street_name'),
        postal_code=data.get('postal_code')
    )
    address.save()

    return JsonResponse({'message': 'Address created successfully', 'data': address.to_dict()}, status=201)


@require_http_methods(["PUT"])
def update_address(request, user_id):
    """ Update an existing address for a user. """
    try:
        user = User.objects.get(id=user_id)
        address = user.address # type: ignore
        if not address.exists():
            return JsonResponse({'error': 'Address not found'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    data = json.loads(request.body.decode('utf-8'))
    for field in ['city', 'state', 'local_government_area', 'nearest_bus_stop',
                  'house_number', 'street_name', 'postal_code']:
        if field in data:
            setattr(address, field, data[field])

    address.updated_at = datetime.now()
    address.save()
    return JsonResponse({'message': 'Address updated successfully', 'data': address.to_dict()}, status=200)

# Note: The delete_address function is not implemented because every user should have an address.
# Hence, deleting an address would not be appropriate in this context.
