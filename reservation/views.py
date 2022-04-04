from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json
from django.utils.dateparse import parse_datetime
from django.core import serializers

from .models import *
from .errors import *
from .const import *
from django.contrib.auth.decorators import login_required
from ctypes.test.test_pickling import name

from django.core.mail import send_mail

@login_required
def index(request):
    zone_list = Zone.list_all()
    return render(request, "index.html", {
        "zone_list": zone_list,
    })

@login_required
def usermng_staff(request):
    staff_list = User.list_staff(ROLE_STAFF)
    return render(request, "staff_index.html", {
        "staff_list": staff_list,
    })

@csrf_exempt
def user_delete(request):
    if request.method == 'GET':
        params = request.GET

        # Check required fields
        if 'id' not in params:
            return JsonResponse({
                "error_code": ERR_MISSING_REQUIRED_FIELD_CODE,
                "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG
            })

        #Check if admin or staff
        
        User.delete(params['id'])

        return JsonResponse({
            "error_code": 0,
        })

@login_required
def usermng_leader(request):
    leader_list = User.list_staff(ROLE_LEAD)
    return render(request, "leader_index.html", {
        "leader_list": leader_list,
    })

@login_required
def usermng_member(request):
    member_list = User.list_staff(ROLE_MEMBER)
    return render(request, "member_list.html", {
        "member_list": member_list,
    })

@login_required
def authority_detail(request, id):
    user = User.findUserById(id)
    team_list = Team.list_all(0)
    return render(request, "authority_detail.html", {
        "userDetail": user,
        "team_list": team_list,
    })
@login_required
def authority_udpate(request):
    team_list = Team.list_all(0)
    if request.method == 'GET':
        params = request.GET
    userId = params['userId']
    roleId = params['roleId']
    teamId = params['teamId']
    user = User.findUserById(userId).first()
    print(user.role_id.id)
    #if roleId == ROLE_STAFF :
    #    print("~~~~~~")
    user.role_id.id = roleId
    print(user.username)
    print(user.role_id.id)
    user.save()

    #if(roleId == ROLE_LEAD):
    #    team_m = TeamMember(team_id = teamId, user_id = userId)
    #    team_m.save()
    #    user.role_id.id = roleId
    #    user.save();

    return render(request, "authority_detail.html", {
        "userDetail": user,
        "team_list": team_list,
    })
    
@login_required
def authority_user(request):
    user_list = User.list_all(0)
    team_list = Team.list_all(0)

    #send_mail('Test email', 'First Django email by QQ', '394887350@qq.com', ['hibernatehou@tamu.edu'], fail_silently=False)

    email_list = []

    for r in user_list:
        email_list.append({
            "name": r.email,
        })

    return render(request, "authority_user.html", {
        "user_list": user_list,
        "team_list": team_list,
        "email_list": email_list,
    })

# POST https://console.aws.amazon.com/cloud9/ide/79b97093f17f4c9ab2bb12c9205ebaf7/create
# {
# user_id: ...    
#}
@csrf_exempt 
def reservation_create(request):
    try:
        if request.method == 'POST':
            #print(str(request.body))
            params = json.loads(request.body)
            #print(params)
            # Check required fields
            if 'zone_id' not in params or 'zone_name' not in params or 'is_long_term' not in params or 'title' not in params or 'reservation_type' not in params or 'start_time' not in params or 'end_time' not in params or 'user_id' not in params:
                return JsonResponse({
                    "error_code": ERR_MISSING_REQUIRED_FIELD_CODE,
                    "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG
                })
                
            
            # Validate fields
            reservation = Reservation(zone_id = params['zone_id'], zone_name = params['zone_name'], is_long_term = params['is_long_term'], title = params['title'], reservation_type = params['reservation_type'], start_time = parse_datetime(params['start_time']),
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
    except Exception as e:
        return JsonResponse({
            "error_code": ERR_INTERNAL_ERROR_CODE,
            "error_message": str(e),
        })
        
        

def reservation_history(request):
    reservations = Reservation.list_all(0)
    return render(request, "reservation_history.html", {
       "reservations": reservations,
    })
        
        
def reservation_list(request):
    if request.method == 'GET':
        params = request.GET
        
        # Check required fields
        if 'user_id' not in params:
            reservations = Reservation.list_all()
        else:
            reservations = Reservation.list_all(params['user_id'])
                
        ret = []

        for r in reservations:
            ret.append({
                "id": r.id,
                "title": r.title,
                "description": r.description,
                "zone_id": r.zone_id,
                "zone_name": r.zone_name,
                "user_id": r.user_id,
                "team_id": r.team_id,
                "is_long_term": r.is_long_term,
                "start_time": r.start_time,
                "end_time": r.end_time,
                "reservation_type": r.reservation_type,
            })
                
        return JsonResponse({
            "error_code": 0,
            "results": ret
        })
        
@csrf_exempt
def reservation_delete(request):
    if request.method == 'GET':
        params = request.GET

        # Check required fields
        if 'id' not in params:
            return JsonResponse({
                "error_code": ERR_MISSING_REQUIRED_FIELD_CODE,
                "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG
            })

        Reservation.delete(params['id'])

        return JsonResponse({
            "error_code": 0,
        })
        
def zone_list(request):
    if request.method == 'GET':
        zones = Zone.list_all()
        results = []
        
        for zone in zones:
            results.append({
                "id": zone.id,
                "name": zone.name,
                "is_noisy": zone.is_noisy,
                "description": zone.description,
                "zone_type": zone.zone_type,
            })
        
        return JsonResponse({
            "error_code": 0,
            "results": results,
        })
        
        
# team view
def team_view(request):
    if request.method == 'GET':
        if request.user.role_id.id == ROLE_ADMIN or request.user.role_id.id == ROLE_STAFF:
            teams = Team.list_all()
            team_list_title = 'Team List'
        else:
            teams = Team.list_all(request.user.id)
            team_list_title = 'My Teams'
        return render(request, "team_list.html", {
            "teams": teams,
            "team_list_title": team_list_title,
        })
    
def team_detail(request, team_id):
    members = TeamMember.get_team_members(team_id)
    return render(request, "team_detail.html", {
        "members": members
    })
    
    
def team_details_update(request, tid):
    try:
        if request.method == 'POST':
            # [TODO] fill out the steps to update team details.
            return JsonResponse({"error_code": 0,});
    except Exception as e:
        return JsonResponse({
            "error_code": ERR_INTERNAL_ERROR_CODE,
            "error_msg": str(e),
        })
    
@csrf_exempt
def team_delete(request):
    if request.method == 'GET':
        params = request.GET
        
        # Check required fields
        if 'id' not in params:
            return JsonResponse({
                "error_code": ERR_MISSING_REQUIRED_FIELD_CODE,
                "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG
            })
    
        Team.delete(params['id'])
        
        return JsonResponse({
            "error_code": 0,
        })
        
@csrf_exempt 
def team_create(request):
    try:
        if request.method == 'POST':
            params = json.loads(request.body)

            # Check required fields
            if 'name' not in params:
                return JsonResponse({
                    "error_code": ERR_MISSING_REQUIRED_FIELD_CODE,
                    "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG
                })
                
            # Create team
            team = Team(name = params['name'])
            team.save()
            return JsonResponse({
                "error_code": 0, 
                "team_id": team.id, 
                "team_name": team.name
            })
    except Exception as e:
        return JsonResponse({
            "error_code": ERR_INTERNAL_ERROR_CODE,
            "error_msg": str(e),
            # I don't know reservation_create why here is error_message instead error_msg. Is that just a typo?
        })

@csrf_exempt
def training_view(request):
    if request.method == 'GET':
        if request.user.role_id.id == ROLE_ADMIN or request.user.role_id.id == ROLE_STAFF:
            training = Training.list_all()
            training_list_title = 'Training List'
        else:
            training = Training.list_all(request.user.id)
            training_list_title = 'My Training'
        return render(request, "training_list.html", {
            "training": training,
            "training_list_title": training_list_title,
        })

@csrf_exempt
def training_delete(request):
    if request.method == 'GET':
        params = request.GET
        
        # Check required fields
        if 'id' not in params:
            return JsonResponse({
                "error_code": ERR_MISSING_REQUIRED_FIELD_CODE,
                "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG
            })
    
        Training.delete(params['id'])
        
        return JsonResponse({
            "error_code": 0,
        })

@csrf_exempt 
def training_create(request):
    try:
        if request.method == 'POST':
            params = json.loads(request.body)

            # Check required fields
            if 'name' not in params:
                return JsonResponse({
                    "error_code": ERR_MISSING_REQUIRED_FIELD_CODE,
                    "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG
                })
                
            # Create team
            training = Training(name = params['name'])
            training.save()
            return JsonResponse({
                "error_code": 0, 
                #"team_id": team.id, 
                #"team_name": team.name
            })
    except Exception as e:
        return JsonResponse({
            "error_code": ERR_INTERNAL_ERROR_CODE,
            "error_msg": str(e),
            # I don't know reservation_create why here is error_message instead error_msg. Is that just a typo?
        })