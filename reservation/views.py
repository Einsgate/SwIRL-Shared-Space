from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

import json
from django.utils.dateparse import parse_datetime

from .models import Reservation

def index(request):
    t = loader.get_template('index.html')
    return HttpResponse(t.render())

def reservation_create(request):
    if request.method == 'POST':
        body = json.load(request.body)
        
        # Check required fields
        if 'title' not in body or 'type' not in body or 'start_time' not in body or 'end_time' not in body or 'user_id' not in body:
            return render(request, 'index.html', {
                "error_code": 1000,
                "error_msg": "Missing required fields"
            })
            
        
        # Validate fields
        reservation = Reservation(title = body['title'], reservation_type = body['reservation_type'], start_time = parse_datetime(body['start_time']),
            end_time = parse_datetime(body['end_time']), user_id = body['user_id'])
        if not reservation.is_valid():
            return render(request, 'index.html', {
                "error_code": 1001,
                "error_msg": "Field value error"
            })
            
        # Check conflicts
        if reservation.has_confliction():
            return render(request, 'index.html', {
                "error_code": 1002,
                "error_msg": "Conflit with existing reservations"
            })
            
        # Create reservation
        reservation.save()
        return render(request, 'index.html', {
            "error_code": 0,
            "id": reservation.id
        })