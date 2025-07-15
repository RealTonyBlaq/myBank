from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
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
    NIN = data.get('NIN')
    title = data.get('title')

    if not BVN and not NIN:
        return JsonResponse({'error': 'Either BVN or NIN must be provided'}, status=400)

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

    return JsonResponse({
        'message': 'User created', 'data': new_user.to_dict()}, status=201)
