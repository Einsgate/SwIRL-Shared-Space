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
    #teamId = params['teamId']
    user = User.findUserById(userId)
    if roleId == '1' :
        role = Role.findById(ROLE_STAFF)
        user.role_id = role
        user.save()

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
            users = User.list_all()
            teams = Team.list_all()
            team_list_title = 'Team List'
        else:
            teams = Team.list_all(request.user.id)
            team_list_title = 'My Teams'
        return render(request, "manage-team/team_list.html", {
            "users": users, 
            "teams": teams,
            "team_list_title": team_list_title,
        })
    
# update the name and leader of a team
@csrf_exempt
def team_view_update(request):
    try:
        if request.method == 'GET':
            team_id = request.GET.get('team_id')
            team = Team.query(team_id)
            teammembers = TeamMember.get_team_members(team_id)
            team_name = team.name;
            if team.leader_id == None:
                team_leader_id = -1
            else:
                team_leader_id = team.leader_id.id
            teammembers_user_id = [[teammember.user_id.id,  teammember.user_id.username, teammember.user_id.email] for teammember in teammembers]
            return JsonResponse({
                "error_code": 0, 
                "team_name": team_name, 
                "team_leader_id": team_leader_id, 
                "members": teammembers_user_id, 
            });
            
        if request.method == 'POST':
            params = json.loads(request.body)
            if 'team_id' not in params:
                return JsonResponse({
                    "error_code": ERR_MISSING_REQUIRED_FIELD_CODE, 
                    "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG, 
                });
                
            team = Team.query(params['team_id']);
                
            # update the team name
            updated = False;
            if 'team_name' in params: 
                new_team_name = params['team_name']
                if new_team_name != team.name:
                    updated = True
                    team.name = new_team_name
                    
            print(params['team_leader_id'] == "-1", params['team_leader_id']);
            
            new_team_leader_id = "-1"
            new_team_username = ""
            if 'team_leader_id' in params and params['team_leader_id'] != "-1":
                new_team_leader_id = params['team_leader_id']
                print(new_team_leader_id)
                new_team_leader = User.query(new_team_leader_id)
                new_team_username = new_team_leader.username
                if team.leader_id == None or new_team_leader_id != team.leader_id.id:
                    updated = True
                    team.leader_id = new_team_leader
                    
            if updated:
                team.save();

            return JsonResponse({
                "error_code": 0,
                "new_team_leader_id": new_team_leader_id, 
                "new_team_leader_username": new_team_username, 
            });
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
            params = json.loads(request.body)
            if 'name' not in params:
                return JsonResponse({
                    "error_code": ERR_MISSING_REQUIRED_FIELD_CODE, 
                    "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG, 
                });
                
            new_team_name = params['name']
            
            # Create a team
            if 'leader_id' in params and params['leader_id'] != '-1':
                print(params)
                new_team_leader = User.query(params['leader_id'])
                team = Team(name = new_team_name, leader_id = new_team_leader)
                team.save()
                
                teammember = TeamMember(team_id = team, user_id = new_team_leader)
                teammember.save();
                return JsonResponse({
                    "error_code": 0,
                    # "team_id": team.id, 
                    # "new_team_name": new_team_name, 
                    # "new_team_leader": new_team_leader, 
                });
            else:
                team = Team(name = new_team_name)
                team.save()
                return JsonResponse({
                    "error_code": 0, 
                    # "team_id": team.id, 
                    # "team_name": team.name
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
            # Check required fields
            params = json.loads(request.body)
            print("L423: ", params)
            if 'zoneId' not in params or 'name' not in params or 'startDate' not in params or 'endDate' not in params:
                return JsonResponse({
                    "error_code": ERR_MISSING_REQUIRED_FIELD_CODE, 
                    "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG, 
                });
            training = Training(name = params['name'], description = params['desc'], start_time = parse_datetime(params['startDate']), end_time = parse_datetime(params['endDate']), zone_id = params['zoneId'], instructor_id = params['instructorId'])
            training.save()
            return JsonResponse({
                "error_code": 0,
                "training_id": training.id,
                "training_name": training.name,
                "training_description": training.description,
                "training_instructor_id": training.instructor_id,
                "training_start_time": training.start_time,
                "training_end_time": training.end_time,
                "training_zone_id": training.zone_id
            })
    except Exception as e:
        return JsonResponse({
            "error_code": ERR_INTERNAL_ERROR_CODE,
            "error_msg": str(e),
            # I don't know reservation_create why here is error_message instead error_msg. Is that just a typo?
        })

@csrf_exempt
def training_apply_view(request):
    if request.method == 'GET':
        if request.user.role_id.id == ROLE_ADMIN or request.user.role_id.id == ROLE_STAFF:
            my_training = My_Training.list_all()
            my_training_list_title = 'All Apply Training List'
        else:
            my_training = My_Training.list_all(request.user.id)
            my_training_list_title = 'My Training Apply'
        return render(request, "training_apply.html", {
            "training": my_training,
            "training_list_title": my_training_list_title,
        })
    
@csrf_exempt
def training_apply(request):
    try:
        if request.method == 'POST':
            # Check required fields
            params = json.loads(request.body)
            print(params)
            if 'zone_id' not in params or 'user_id' not in params or 'start_time' not in params or 'end_time' not in params:
                return JsonResponse({
                    "error_code": ERR_MISSING_REQUIRED_FIELD_CODE, 
                    "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG, 
                });
            my_training = My_Training(name = params['name'], user_id = params['user_id'], start_time = parse_datetime(params['start_time']), end_time = parse_datetime(params['end_time']), zone_id = params['zone_id'])
            my_training.save()
            return JsonResponse({
                "error_code": 0,
            })
    except Exception as e:
        return JsonResponse({
            "error_code": ERR_INTERNAL_ERROR_CODE,
            "error_msg": str(e),
            # I don't know reservation_create why here is error_message instead error_msg. Is that just a typo?
        })

@csrf_exempt
def training_apply_delete(request):
    if request.method == 'GET':
        params = request.GET
        
        # Check required fields
        if 'id' not in params:
            return JsonResponse({
                "error_code": ERR_MISSING_REQUIRED_FIELD_CODE,
                "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG
            })

        My_Training.delete(params['id'])

        return JsonResponse({
            "error_code": 0,
        })

def team_detail(request, team_id):
    members = TeamMember.get_team_members(team_id)
    not_members = User.list_not_members(team_id)
    team = Team.query(team_id)
    team_name = team.name
    if team.leader_id == None:
        team_leader_id = -1
    else:
        team_leader_id = team.leader_id.id
    return render(request, "manage-team/team_detail.html", {
        "team_id": team_id, 
        "team_name": team_name, 
        "team_leader_id": team_leader_id, 
        "not_members": not_members, 
        "members": members
    })
    
@csrf_exempt    
def team_detail_update(request, team_id):
    try:
        if request.method == 'POST':
            params = json.loads(request.body)
            if 'selected_members' not in params:
                return JsonResponse({
                    "error_code": ERR_MISSING_REQUIRED_FIELD_CODE, 
                    "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG, 
                })
                
            for user_id in params['selected_members']:
                TeamMember.objects.get_or_create(user_id = User.query(user_id), team_id = Team.query(team_id))
                
            return JsonResponse({"error_code": 0,});
    except Exception as e:
        return JsonResponse({
            "error_code": ERR_INTERNAL_ERROR_CODE,
            "error_msg": str(e),
        })
        
@csrf_exempt  
def team_detail_delete(request, team_id): 
    if request.method == 'GET':
        params = request.GET
        
        # Check required fields
        if 'id' not in params:
            return JsonResponse({
                "error_code": ERR_MISSING_REQUIRED_FIELD_CODE,
                "error_msg": ERR_MISSING_REQUIRED_FIELD_MSG
            })
        
        teammember = TeamMember.query(params['id'])
        team = teammember.team_id
    
        if team.leader_id == teammember.user_id: 
            team.leader_id = None
            team.save();
        
        teammember.delete();
        
        return JsonResponse({
            "error_code": 0,
        })

