import json

from django.db import IntegrityError, transaction
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from users.models import User 
from .models import Pereval, PerevalImage, PerevalLevel, Coordinates
from .utils import check_fields

@csrf_exempt
def submitData(request):

    if request.method != 'POST':

        return JsonResponse({'status':400,  'message':f'Method {request.method} not allowed!', 'id': None})
    
    data =json.loads(request.body)

    try:
        check_fields(data)
    except KeyError as ex:
        return JsonResponse({'status':400, 'message': ex.__str__(), 'id': None})
    
    try:
        with transaction.atomic():

            user=User.objects.get_or_create(**data['user'])[0]
            coords=Coordinates.objects.create(
                latitude=float(data['coords']['latitude']),
                longitude=float(data['coords']['longitude']),
                height=int(data['coords']['height']),
                )
            level=PerevalLevel.objects.create(**data['level'])

            pereval = Pereval.objects.create(
                beautyTitle=data['beauty_title'],
                title=data['title'],
                other_titles=data['other_titles'],
                connect=data['connect'],
                add_time=data['add_time'],
                user=user,
                coords=coords,
                level=level
            )

            # TODO с файлами чето сделать надо
            for image in data['images']:

                PerevalImage.objects.create(
                    to_pereval=pereval,
                    title=image['title'],
                    image=image['data'])


    except ValueError as ex:
        return JsonResponse({'status': 400, 'messsge': ex.__str__(), 'id': None})

    except Exception as ex:
        return JsonResponse({'status': 500, 'message': ex.__str__(), 'id': None})
    
    return JsonResponse({'status': 200, 'message': None, 'id': pereval.id})