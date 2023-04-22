Sure, here's the transformed API code in Django:

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from rest_framework import status
from .. import models, schemas, utils

@csrf_exempt
@transaction.atomic
def create_user(request):
    if request.method == 'POST':
        user_data = json.loads(request.body)
        user = schemas.UserCreate(**user_data)
        
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        
        exist = models.User.objects.filter(email=user.email).first()
        if exist is not None:
            return JsonResponse({"detail": f"This email: {user.email} is already registered. Please use another email or renew your password for this one."}, status=status.HTTP_409_CONFLICT)
        
        exist = models.User.objects.filter(username=user.username).first()
        if exist is not None:
            return JsonResponse({"detail": f"This username: {user.username} is already taken. Please choose another username."}, status=status.HTTP_409_CONFLICT)
        
        db_user = models.User(**user_data)
        db_user.save()
        return JsonResponse(db_user, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({"detail": "Invalid request method."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

Note: Please make sure to import the necessary models, schemas, and utils modules in the Django view. Also, you may need to modify the view function to fit your specific Django project structure.