from django.db import IntegrityError, transaction
from django.http.response import JsonResponse

from .utils import check_fields

def submitData(request):

    if request.method != 'POST':

        return JsonResponse({'status':400,  'message':f'Method {request.method} not allowed!', 'id': None})
    
    data = request.POST.dict()

    try:
        check_fields(data)
    except KeyError as ex:
        return JsonResponse({'status':400, 'message': ex.__str__(), 'id': None})