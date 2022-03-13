from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def create_reservation(request):
    error_code = request.POST.get('error_code', None)
    error_msg = request.POST.get('error_msg', None)
    data = {
        'error_code': error_code, 
        'error_msg': error_msg
    };
    return JsonResponse(data);
            