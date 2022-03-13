from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json
from django.utils.dateparse import parse_datetime

from .models import Reservation
from .errors import *

def index(request):
    t = loader.get_template('index.html')
    return HttpResponse(t.render())

# POST https://console.aws.amazon.com/cloud9/ide/79b97093f17f4c9ab2bb12c9205ebaf7/create
# {
# user_id: ...    
#}
@csrf_exempt 
def reservation_create(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        
        # Check required fields
        if 'title' not in params or 'reservation_type' not in params or 'start_time' not in params or 'end_time' not in params or 'user_id' not in params:
            return JsonResponse({
                "error_code": ERR_MISSING_REQUIRED_FIELD_CODE,
                "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG
            })
            
        
        # Validate fields
        reservation = Reservation(title = params['title'], reservation_type = params['reservation_type'], start_time = parse_datetime(params['start_time']),
            end_time = parse_datetime(params['end_time']), user_id = params['user_id'])
        if not reservation.is_valid():
            return JsonResponse({
                "error_code": ERR_VALUE_ERROR_CODE,
                "error_msg": ERR_VALUE_ERROR_MSG
            })
            
        # Check conflicts
        if reservation.has_confliction():
            return JsonResponse({
                "error_code": ERR_RESERVATION_CONFLICT_CODE,
                "error_msg": ERR_RESERVATION_CONFLICT_MSG
            })
            
        # Create reservation
        reservation.save()
        return JsonResponse({
            "error_code": 0,
            "id": reservation.id
        })
        
def reservation_list(request):
    if request.method == 'GET':
        params = request.GET
        
        # Check required fields
        if 'user_id' not in params:
            return render(request, 'index.html', {
                "error_code": ERR_MISSING_REQUIRED_FIELD_CODE,
                "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG
            })
            
        return render(request, 'index.html', {
            "error_code": 0,
            "results": Reservation.list_all(params['user_id'])
        })
        
        
def reservation_delete(resquest):
    if request.method == 'GET':
        params = request.GET
        
        # Check required fields
        if 'id' not in params:
            return render(request, 'index.html', {
                "error_code": ERR_MISSING_REQUIRED_FIELD_CODE,
                "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG
            })
            
        Reservation.delete(params['id'])
            
        return render(request, 'index.html', {
            "error_code": 0,
        })