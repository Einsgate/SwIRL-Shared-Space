from django.test import TestCase
from .models import *

from django.test import Client
import json
from dateutil import parser
from pytz import timezone

from .models import *
from .const import *
from .errors import *
import numpy as np
import random
import os

from django.urls import reverse
from django.core.exceptions import PermissionDenied

# Create your tests here.

SHARED_SPACE_ADMIN_PASSWORD = os.environ['SHARED_SPACE_ADMIN_PASSWORD']

class TestData(object):
    def init_database(self):
        self.role_admin = Role.objects.get(id = 0)
        self.role_staff = Role.objects.get(id = 1)
        self.role_team_leader = Role.objects.get(id = 2)
        self.role_member = Role.objects.get(id = 3)
        
         # Test data
        self.test_member_1 = User(username = 'test_member_1', email = 'test_member_1@tamu.edu', is_active = True, is_superuser = True, is_staff = True, role_id = self.role_member)
        self.test_member_1.set_password('123')
        self.test_member_1.save()
        
        self.test_member_2 = User(username = 'test_member_2', email = 'test_member_2@tamu.edu', is_active = True, is_superuser = True, is_staff = True, role_id = self.role_member)
        self.test_member_2.set_password('123')
        self.test_member_2.save()
        
        #UserModel = apps.get_model('reservation', 'User')
        User.objects.create(username = "test_admin_1", email = "test_admin_1@tamu.edu", role_id = self.role_admin)
        User.objects.create(username = "test_admin_2", email = "test_admin_2@tamu.edu", role_id = self.role_admin)
        User.objects.create(username = "test_staff_1", email = "test_staff_1@tamu.edu", role_id = self.role_staff)
        User.objects.create(username = "test_staff_2", email = "test_staff_2@tamu.edu", role_id = self.role_staff)
        #User.objects.create(id = 3, username = "test_lead_1", email = "test_lead_1@tamu.edu", role_id = 2)
        #User.objects.create(id = 3, username = "test_lead_2", email = "test_lead_2@tamu.edu", role_id = 2)
        #user5 = UserModel.objects.create(username = "test_member_1", email = "test_member_1@tamu.edu", role_id = 2)
        self.test_member_1 = User.objects.get(username = "test_member_1")
        self.test_member_2 = User.objects.get(username = "test_member_2")
        self.test_member_3 = User.objects.create(username = "test_member_3", email = "test_member_3@tamu.edu", role_id = self.role_member)
        User.objects.create(username = "test_member_4", email = "test_member_4@tamu.edu", role_id = self.role_member)
        User.objects.create(username = "test_member_5", email = "test_member_5@tamu.edu", role_id = self.role_member)
    
    
       # Team = apps.get_model('reservation', 'Team')
        self.team1 = Team.objects.create(name = "test_team_1", leader_id = self.test_member_1)
        Team.objects.create(name = "test_team_2")
        
        #TeamMember = apps.get_model('reservation', 'TeamMember')
        TeamMember.objects.create(team_id = self.team1, user_id = self.test_member_1)
        TeamMember.objects.create(team_id = self.team1, user_id = self.test_member_2)
        TeamMember.objects.create(team_id = self.team1, user_id = self.test_member_3)

# Test modals
class ReservationTestCase(TestCase, TestData):
    def setUp(self):
        self.c = Client()

        self.init_database()
        #Reservation.objects.create(title = 'setup1', reservation_type = 0, start_time = '2000-01-01 12:00:00', end_time = '2000-01-01 12:30:00', user_id = 1)

    def test_is_valid(self):
        reservation1 = Reservation(reservation_type = 1, start_time = '2022-01-01 13:00:00', user_id = self.test_member_1, team_id = self.team1, 
            end_time = '2022-01-01 14:00:00')
        reservation2 = Reservation(reservation_type = 0, start_time = '2022-01-01 13:00:00', user_id = self.test_member_1, team_id = self.team1,
            end_time = '2022-01-01 14:00:00')
        reservation3 = Reservation(reservation_type = 1, start_time = '2022-01-01 15:00:00', user_id = self.test_member_1, team_id = self.team1,
            end_time = '2022-01-01 14:00:00')
        
        self.assertEqual(reservation1.is_valid(), True)
        self.assertEqual(reservation2.is_valid(), False)
        self.assertEqual(reservation3.is_valid(), False)
        
        
    def test_has_confliction(self):
        Reservation.objects.create(zone_id = 1, reservation_type = 1, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00')
        Reservation.objects.create(zone_id = 2, reservation_type = 2, start_time = '2000-01-02 12:00:00', end_time = '2000-01-02 12:30:00')
        
        self.assertEqual(Reservation(zone_id = 1, reservation_type = 1, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00').has_confliction()[0], True)
        self.assertEqual(Reservation(zone_id = 3, reservation_type = 1, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00').has_confliction()[0], False)
        self.assertEqual(Reservation(zone_id = 3, reservation_type = 1, start_time = '2000-01-02 12:00:00', end_time = '2000-01-02 12:30:00').has_confliction()[1], True)
        self.assertEqual(Reservation(zone_id = 3, reservation_type = 2, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00').has_confliction()[0], False)

        
        #response = c.post('/reservation/create', {'title': "test", "reservation_type": 0, start_time = 'xxx', end_time = "xxx"})
        
    def test_create_success(self):
        self.c.login(username='admin', password=SHARED_SPACE_ADMIN_PASSWORD)
        #self.c.login(username='test_member_1', password='123')
        
        resp = self.c.post('/reservation/create', json.dumps({
            'title': 'test', 
            'reservation_type': 3, 
            'zone_id': 1, 
            'zone_name': 'zone 1', 
            'start_time': '2022-03-14 12:00:00', 
            'end_time': '2022-03-14 13:00:00', 
            'team_id': self.team1.id,
            
        }), content_type="application/json")
        
        # self.assertEqual(resp.status_code, 200)
        print(resp.content)
        data = json.loads(resp.content)
        self.assertEqual(data["error_code"], 0)
        
       
    def test_create_fail(self):
        self.c.login(username='admin', password=SHARED_SPACE_ADMIN_PASSWORD)
        
        resp = self.c.post('/reservation/create', json.dumps({
            'title': 'test', 
            'reservation_type': 1, 
            'zone_id': 1, 
            'zone_name': 'zone 1', 
            'start_time': '2022-03-14 12:00:00', 
            'end_time': '2022-03-14 13:00:00', 
            'team_id': self.team1.id,
            
        }), content_type="application/json")
        
        # self.assertEqual(resp.status_code, 200)
        print(resp.content)
        data = json.loads(resp.content)
        self.assertEqual(data["error_code"], 0)
        
        
        # Since this reservation is conflicted with the previous one, it should fail
        resp = self.c.post('/reservation/create', json.dumps({
            'title': 'test', 
            'reservation_type': 1, 
            'zone_id': 1, 
            'zone_name': 'zone 1', 
            'start_time': '2022-03-14 12:00:00', 
            'end_time': '2022-03-14 14:00:00', 
            'team_id': self.team1.id,
            
        }), content_type="application/json")
        
        # self.assertEqual(resp.status_code, 200)
        print(resp.content)
        data = json.loads(resp.content)
        self.assertNotEqual(data["error_code"], 0)  # Should fail (ereor_code != 0)
    
        # Fail since missing required field
        resp = self.c.post('/reservation/create', json.dumps({
            'title': 'test', 
            'reservation_type': 1, 
            'zone_name': 'zone 1', 
            'start_time': '2022-03-14 12:00:00', 
            'end_time': '2022-03-14 14:00:00', 
            'team_id': self.team1.id,
            
        }), content_type="application/json")
        
        # self.assertEqual(resp.status_code, 200)
        print(resp.content)
        data = json.loads(resp.content)
        self.assertNotEqual(data["error_code"], 0)  # Should fail (ereor_code != 0)
        
        # Fail since wrong field value
        resp = self.c.post('/reservation/create', json.dumps({
            'title': 'test', 
            'reservation_type': 4, 
            'is_long_term': False,
            'zone_id': 1, 
            'zone_name': 'zone 1', 
            'start_time': '2022-03-14 12:00:00', 
            'end_time': '2022-03-14 14:00:00', 
            'team_id': self.team1.id,
            
        }), content_type="application/json")
        
        # self.assertEqual(resp.status_code, 200)
        print(resp.content)
        data = json.loads(resp.content)
        self.assertNotEqual(data["error_code"], 0)  # Should fail (ereor_code != 0)
    
    def test_list(self):
        Reservation.objects.all().delete()
        reservations = [
            Reservation(zone_id = 1, reservation_type = 1, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00', user_id = self.test_member_1, team_id = self.team1,),
            Reservation(zone_id = 2, reservation_type = 3, start_time = '2000-01-02 12:00:00', end_time = '2000-01-02 12:30:00', user_id = self.test_member_1, team_id = self.team1,),
            Reservation(zone_id = 3, reservation_type = 2, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00', user_id = self.test_member_1, team_id = self.team1,),
            Reservation(zone_id = 4, reservation_type = 1, start_time = '2000-01-02 12:00:00', end_time = '2000-01-02 12:30:00', user_id = self.test_member_1, team_id = self.team1,),
        ]

        for r in reservations:
            r.save()
        
        resp = self.c.get('/reservation/list')
        
        # self.assertEqual(resp.status_code, 200)
        print(resp.content)
        data = json.loads(resp.content)
        self.assertEqual(data["error_code"], 0)  # error_code = 0
        
        print(data)
        results = data["results"]
        for i, r in enumerate(results):
            self.assertEqual(r["zone_id"], reservations[i].zone_id) 
            self.assertEqual(r["reservation_type"], reservations[i].reservation_type) 
            
            # Both Convert to UTC time
            list_start_time, start_time = parser.parse(r["start_time"]).replace(tzinfo=timezone('UTC')), parser.parse(reservations[i].start_time).replace(tzinfo=timezone('UTC'))
            list_end_time, end_time = parser.parse(r["end_time"]).replace(tzinfo=timezone('UTC')), parser.parse(reservations[i].end_time).replace(tzinfo=timezone('UTC'))
            self.assertEqual(list_start_time == start_time, False) 
            self.assertEqual(list_end_time == end_time, False)
            self.assertEqual(r["user_id"], reservations[i].user_id.id) 
        
    def test_delete(self):
        Reservation.objects.all().delete()
        reservations = [
            Reservation(zone_id = 1, reservation_type = 1, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00', user_id = self.test_member_1, team_id = self.team1,),
            Reservation(zone_id = 2, reservation_type = 1, start_time = '2000-01-02 12:00:00', end_time = '2000-01-02 12:30:00', user_id = self.test_member_1, team_id = self.team1,),
            Reservation(zone_id = 3, reservation_type = 2, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00', user_id = self.test_member_1, team_id = self.team1,),
            Reservation(zone_id = 4, reservation_type = 1, start_time = '2000-01-02 12:00:00', end_time = '2000-01-02 12:30:00', user_id = self.test_member_1, team_id = self.team1,),
        ]
        
        id = 0
        for r in reservations:
            r.save()
            id = r.id
            
        self.assertEqual(len(Reservation.objects.filter(id=id)), 1)
        
        # Delete reservation with the given id
        resp = self.c.get('/reservation/delete', {'id': id})
        # self.assertEqual(resp.status_code, 200)
        print(resp.content)
        data = json.loads(resp.content)
        self.assertEqual(data["error_code"], 0)  # error_code = 0
        
        # Check if it is deleted
        self.assertEqual(len(Reservation.objects.filter(id=id)), 0)

    # def test_zone_list(self):
    #     self.c.login(username='admin', password=SHARED_SPACE_ADMIN_PASSWORD)
    #     resp = self.c.get('/zone/list')
    #     self.assertEqual(resp.status_code, 200)
        
    #     data = json.loads(resp.content)
    #     self.assertEqual(data["error_code"], 0)  


# Initialize the database to have 8 users and 7 teams, where 
# User 0 is the admin and User 1 is the staff. Team 0 and Team 1 have the leader_id = None.
# User start from 2 only belongs to team with the user index | team index, Thus Team 0 has 
# all users, and Team 1 has no members. Teams start from 2 has the leader with user index =
# team index. Note that User 0 (the admin) and User 1 (the staff) aren't in any teams.
def init_users_and_teams():
    # Clear the database except Role
    User.objects.all().delete()
    Team.objects.all().delete()
    TeamMember.objects.all().delete()
    Role.objects.all().delete()
    
    num_users = 6
    num_teams = 5
    role_admin = Role.objects.create(id = 0, role_name = "admin")
    role_admin.save()
    role_staff = Role.objects.create(id = 1, role_name = "staff")
    role_staff.save()
    role_member = Role.objects.create(id = ROLE_MEMBER, role_name = "member")
    role_member.save()

    # Initialize users.
    test_users = [
        User.objects.create(username = 'test_user_admin', email = 'test_user_admin@gmail.com', is_active = True, is_superuser = True, is_staff = False, role_id = role_admin), 
        User.objects.create(username = 'test_user_staff', email = 'test_user_staff@gmail.com', is_active = True, is_superuser = False, is_staff = False, role_id = role_admin), 
    ]
    test_users[0].set_password('password')
    test_users[0].save()
    test_users[1].set_password('password')
    test_users[1].save()
    for i in range(2, num_users):
        username = 'test_user_%d' %i
        new_user = User.objects.create(username = username, email = username + '@gmail.com', is_active = True, is_superuser = False, is_staff = False, role_id = role_member)
        new_user.set_password('password')
        test_users.append(new_user)
        new_user.save()
        
    # Initialize teams.
    test_teams = [
        Team.objects.create(name = 'test_team_0', leader_id = None), 
        Team.objects.create(name = 'test_team_1', leader_id = None), 
    ]
    test_teams[0].save()
    test_teams[1].save()
    for i in range(2, num_teams):
        team_name = 'test_team_%d' %i
        new_team = Team.objects.create(name = team_name, leader_id = test_users[i])
        test_teams.append(new_team)
        new_team.save()
        
    # Initialize team_members.
    test_team_members = []
    for i in range(2, num_users):
        for j in np.arange(0, num_teams, i):
            new_team_member = TeamMember.objects.create(team_id = test_teams[j], user_id = test_users[i])
            test_team_members.append(new_team_member)
            new_team_member.save()
            
    return test_users, test_teams, test_team_members
    
class TeamTestCase(TestCase):
    
    @classmethod
    def setUp(self):
        self.c = Client()
        self.test_users, self.test_teams, _ = init_users_and_teams()
        self.n_users = len(self.test_users)
        self.n_teams = len(self.test_teams)
        
    def test_list(self):
        self.assertEqual(len(Team.list_all()), self.n_teams)
        self.assertEqual(len(Team.list_all(self.test_users[0].id)), 0)
        
        for i in range(2, self.n_users):
            self.assertEqual(len(Team.list_all(self.test_users[i].id)), (self.n_teams - 1) // i + 1)
        
    def test_query(self):
        for i in range(self.n_teams):
            self.assertEqual(Team.query(self.test_teams[i].id), self.test_teams[i])
        
    def test_delete_team(self):
        # Delete a non-existing id
        Team.delete(self.test_teams[0].id)
        self.assertEqual(Team.list_all().count(), self.n_teams - 1)
        Team.delete(self.test_teams[0].id)
        self.assertEqual(Team.list_all().count(), self.n_teams - 1)
        
        # Delete a random existing id
        tid = self.test_teams[1].id
        team = Team.objects.filter(pk = tid)
        self.assertTrue(team.exists())
        
        Team.delete(tid)
        
        self.assertEqual(Team.list_all().count(), self.n_teams - 2)
        team = Team.objects.filter(pk = tid)
        self.assertFalse(team.exists())
        
class TeamMemberTestCase(TestCase):
    
    @classmethod
    def setUp(self):
        self.c = Client()
        self.test_users, self.test_teams, self.test_team_members = init_users_and_teams()
        self.n_users = len(self.test_users)
        self.n_teams = len(self.test_teams)
        self.n_team_members = len(self.test_team_members)
        
    def test_query(self):
        for i in range(self.n_team_members):
            self.assertEqual(TeamMember.query(self.test_team_members[i].id), self.test_team_members[i])
            
    def test_get_team_members(self):
        for i in range(self.n_teams):
            team_members = TeamMember.get_team_members(team_id = self.test_teams[i].id)
            self.assertEqual(team_members.count(), len([x for x in range(2, self.n_users) if i % x == 0]))
            
    def test_get_by_team_members(self):
        for i in range(self.n_users):
            for j in range(self.n_teams):
                team_members = TeamMember.get_by_team_members(team_id = self.test_teams[j].id, user_id = self.test_users[i].id)
                self.assertEqual( team_members == None, (True if i == 0 or i == 1 or j % i != 0 else False) )
    
# Test views
class TeamListViewTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.c = Client()
        self.test_users, self.test_teams, self.test_team_members = init_users_and_teams()
        self.n_users = len(self.test_users)
        self.n_teams = len(self.test_teams)
        self.n_team_members = len(self.test_team_members)
        
    def test_team_list_url_exists_at_desired_location(self):
        self.c.login(username=self.test_users[0].username, password='password')
        resp = self.c.get('/team/view')
        self.assertEqual(resp.status_code, 200)
        
    def test_team_list_url_accessible_by_name(self):
        self.c.login(username=self.test_users[0].username, password='password')
        resp = self.c.get(reverse('team_view'))
        self.assertEqual(resp.status_code, 200)
        
    def test_team_list_uses_correct_template(self):
        self.c.login(username=self.test_users[0].username, password='password')
        resp = self.c.get(reverse('team_view'))
        self.assertEqual(resp.status_code, 200)
        
        self.assertTemplateUsed(resp, 'manage-team/team_list.html')
    
    def test_admin_staff_view(self): 
        for username in [self.test_users[0].username, self.test_users[1].username]:
            self.c.login(username=username, password='password')
    
            resp = self.c.get(reverse('team_view'))
            self.assertEqual(resp.status_code, 200)
            
            teams = resp.context['teams']
            self.assertEqual(len(teams), self.n_teams)
            
            users = resp.context['users']
            self.assertEqual(len(users), self.n_users - 2) # exclude the admin and the staff
            
            self.assertEqual(resp.context['team_list_title'], 'Team Management')
        
    def test_member_view(self): 
        for i in range(2, self.n_users):
            self.c.login(username=self.test_users[i].username, password='password')
            
            resp = self.c.get(reverse('team_view'))
            # self.assertEqual(resp.status_code, 200)
            
            teams = resp.context['teams']
            self.assertEqual(len(teams), Team.list_all(user_id = self.test_users[i].id).count())
            
            users = resp.context['users']
            self.assertEqual(len(users), 0)
        
            self.assertEqual(resp.context['team_list_title'], 'My Teams')
            
    def test_admin_staff_create_team(self):
        valid_team_name = 'abc'
        valid_leader_id = str(self.test_users[2].id)
        
        # Test the wrong field cases
        post_req_body_list = [
            # Missing the leader_id
            {'name': valid_team_name},       
            # Missing the name
            {'leader_id': valid_leader_id}, 
            # The name is empty
            {'name': '', 'leader_id': valid_leader_id}, 
            # The leader is empty
            {'name': valid_team_name, 'leader_id': ''}, 
            # The leader_id is the admin
            {'name': valid_team_name, 'leader_id': str(self.test_users[0].id)}, 
            # The leader_id is the staff
            {'name': valid_team_name, 'leader_id': str(self.test_users[1].id)}, 
        ]
        
        post_res_code_list = [
            ERR_MISSING_REQUIRED_FIELD_CODE, 
            ERR_MISSING_REQUIRED_FIELD_CODE, 
            ERR_MISSING_TEAM_NAME_CODE, 
            ERR_MISSING_TEAM_LEADER_CODE, 
            ERR_ADMIN_STAFF_TEAM_LEADER_CODE, 
            ERR_ADMIN_STAFF_TEAM_LEADER_CODE, 
        ]
            
        for username in [self.test_users[0].username, self.test_users[1].username]:
            self.c.login(username=username, password='password')
        
            for req_body, res_code in zip(post_req_body_list, post_res_code_list):
                resp = self.c.post(reverse('team_view_create'), json.dumps(req_body), content_type="application/json")
                self.assertEqual(resp.status_code, 200)
                
                data = json.loads(resp.content)
                # print(data['error_msg'])
                self.assertEqual(data['error_code'], res_code)
                
                self.assertEqual(Team.objects.all().count(), self.n_teams)
                self.assertEqual(TeamMember.objects.count(), self.n_team_members)
                
        n_new_teams = 0
        n_new_team_members = 0
        for username in [self.test_users[0].username, self.test_users[1].username]:  
            self.c.login(username=username, password='password')
            
            # Add a new team without no leaders
            new_team_name_1 = 'test_create_team_1_%s' %username
            team_no_leader = {'name': new_team_name_1, 'leader_id': '-1'}
            resp = self.c.post(reverse('team_view_create'), json.dumps(team_no_leader), content_type="application/json")
            n_new_teams += 1
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.content)
            self.assertEqual(data['error_code'], 0)
            self.assertEqual(Team.objects.all().count(), self.n_teams + n_new_teams)
            self.assertEqual(TeamMember.objects.all().count(), self.n_team_members + n_new_team_members)
            
            team = Team.objects.filter(name = new_team_name_1)
            self.assertEqual(team.count(), 1)
            self.assertEqual(team.first().leader_id, None)
            
            # Add a new team with a leader
            new_team_name_2 = 'test_create_team_2_%s' %username
            team_with_leader = {'name': new_team_name_2, 'leader_id': valid_leader_id}
            resp = self.c.post(reverse('team_view_create'), json.dumps(team_with_leader), content_type="application/json")
            n_new_teams += 1
            n_new_team_members += 1
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.content)
            self.assertEqual(data['error_code'], 0)
            self.assertTrue(Team.objects.all().count(), self.n_teams + n_new_teams)
            self.assertTrue(TeamMember.objects.all().count(), self.n_team_members + n_new_team_members)
            
            team = Team.objects.filter(name = new_team_name_2)
            self.assertTrue(team.count(), 1)
            self.assertTrue(team.first().leader_id.id, valid_leader_id)
        
    def test_member_create_team(self): 
        uid = 2
        self.c.login(username=self.test_users[uid].username, password='password')
        resp = self.c.post(reverse('team_view_create'), json.dumps({'name': 'abc', 'leader_id': self.test_users[uid].id}), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['error_code'], ERR_LACK_OF_AUTHORITY_CODE)
        self.assertEqual(Team.objects.all().count(), self.n_teams)
        self.assertEqual(TeamMember.objects.count(), self.n_team_members)
        
    def test_admin_staff_edit_team_get(self):
        uid_list = [0, 1]
        tid_list = [0, 4]
        get_req_body_team_list = [
            # Test get_bodies for test_teams[0]
            [
                # Missing team_id
                {}, 
                {'team_id': str(self.test_teams[tid_list[0]].id), }, 
            ], 
            # Test get_bodies for test_teams[4]
            [
                # Missing team_id
                {}, 
                {'team_id': str(self.test_teams[tid_list[1]].id), }, 
            ]
        ]
        
        get_res_body_team_list = [
            [
                {'error_code': ERR_MISSING_REQUIRED_FIELD_CODE}, 
                {   
                    'error_code': 0, 
                    'team_name': self.test_teams[tid_list[0]].name, 
                    'team_leader_id': -1, 
                    'members': [[m.id, m.username, m.email] for m in self.test_users[2: ]], 
                }, 
            ], 
            [
                {'error_code': ERR_MISSING_REQUIRED_FIELD_CODE}, 
                {   
                    'error_code': 0, 
                    'team_name': self.test_teams[tid_list[1]].name, 
                    'team_leader_id': self.test_teams[tid_list[1]].leader_id.id, 
                    'members': [[m.id, m.username, m.email] for i, m in enumerate(self.test_users[2: ]) if tid_list[1] % (i + 2) == 0], 
                }, 
            ], 
        ]
        
        for uid in uid_list: 
            self.c.login(username=self.test_users[uid].username, password='password')
            # test_teams[0] has all test_users as its members but no lead.
            # test_teams[4] has test_users[2] and test_users[4] as its members and the lead is test_users[2].
            for tid, get_req_body_list, get_res_body_list in zip(tid_list, get_req_body_team_list, get_res_body_team_list):
                
                # Get request
                for req_body, res_body in zip(get_req_body_list, get_res_body_list): 
                    resp = self.c.get(reverse('team_view_update'), req_body)
                    self.assertEqual(resp.status_code, 200)
                    data = json.loads(resp.content)
                    self.assertEqual(data['error_code'], res_body['error_code'])
                    if res_body['error_code'] == 0: 
                        self.assertEqual(data['team_name'], res_body['team_name'])
                        self.assertEqual(data['team_leader_id'], res_body['team_leader_id'])
                        self.assertEqual(sorted(data['members'], key=lambda row: row[0]), sorted(res_body['members'], key=lambda row: row[0]))
        
    def test_admin_staff_edit_team_post(self): 
        uid_list = [0, 1]
        tid_list = [0, 4]
        
        valid_team_name = 'test_abc'
        valid_team_leader_id = self.test_users[4].id
        valid_team_leader_id_str = str(valid_team_leader_id)
        valid_team_leader_user_name = self.test_users[4].username
        post_req_body_team_list = [
            # Test get_bodies for test_teams[0]
            [
                # Missing team_id
                {'team_name': valid_team_name, 'team_leader_id': valid_team_leader_id_str}, 
                # Missing team_name
                {'team_id': str(self.test_teams[tid_list[0]].id), 'team_leader_id': valid_team_leader_id_str}, 
                # Missing team_leader_id
                {'team_id': str(self.test_teams[tid_list[0]].id), 'team_name': valid_team_name}, 
                # Invalid team_leader_id
                {'team_id': str(self.test_teams[tid_list[0]].id), 'team_name': valid_team_name, 'team_leader_id': '-2'}, 
                # Invalid team_leader_id
                {'team_id': str(self.test_teams[tid_list[0]].id), 'team_name': valid_team_name, 'team_leader_id': str(self.test_users[0].id)}, 
                # Invalid team_leader_id
                {'team_id': str(self.test_teams[tid_list[0]].id), 'team_name': valid_team_name, 'team_leader_id': str(self.test_users[1].id)}, 
                # Unchanged team_name
                {'team_id': str(self.test_teams[tid_list[0]].id), 'team_name': '', 'team_leader_id': valid_team_leader_id_str}, 
                # Unchanged team_leader_id
                {'team_id': str(self.test_teams[tid_list[0]].id), 'team_name': valid_team_name, 'team_leader_id': '-1'}, 
                # Unchanged team_leader_id
                {'team_id': str(self.test_teams[tid_list[0]].id), 'team_name': valid_team_name, 'team_leader_id': ''}, 
                # Changed team name and team leader_id
                {'team_id': str(self.test_teams[tid_list[0]].id), 'team_name': valid_team_name, 'team_leader_id': valid_team_leader_id_str}, 
            ], 
            # Test get_bodies for test_teams[4]
            [
                # Missing team_id
                {'team_name': valid_team_name, 'team_leader_id': valid_team_leader_id_str}, 
                # Missing team_name
                {'team_id': str(self.test_teams[tid_list[1]].id), 'team_leader_id': valid_team_leader_id_str}, 
                # Missing team_leader_id
                {'team_id': str(self.test_teams[tid_list[1]].id), 'team_name': valid_team_name}, 
                # Invalid team_leader_id
                {'team_id': str(self.test_teams[tid_list[1]].id), 'team_name': valid_team_name, 'team_leader_id': '-2'}, 
                # Invalid team_leader_id
                {'team_id': str(self.test_teams[tid_list[1]].id), 'team_name': valid_team_name, 'team_leader_id': str(self.test_users[0].id)}, 
                # Invalid team_leader_id
                {'team_id': str(self.test_teams[tid_list[1]].id), 'team_name': valid_team_name, 'team_leader_id': str(self.test_users[1].id)}, 
                # Invalid team_leader_id
                {'team_id': str(self.test_teams[tid_list[1]].id), 'team_name': valid_team_name, 'team_leader_id': str(self.test_users[3].id)}, 
                # Unchanged team_name
                {'team_id': str(self.test_teams[tid_list[1]].id), 'team_name': '', 'team_leader_id': valid_team_leader_id_str}, 
                # Unchanged team_leader_id
                {'team_id': str(self.test_teams[tid_list[1]].id), 'team_name': valid_team_name, 'team_leader_id': '-1'}, 
                # Unchanged team_leader_id
                {'team_id': str(self.test_teams[tid_list[1]].id), 'team_name': valid_team_name, 'team_leader_id': ''}, 
                # Changed team name and team leader_id
                {'team_id': str(self.test_teams[tid_list[1]].id), 'team_name': valid_team_name, 'team_leader_id': valid_team_leader_id_str}, 
            ]
        ]
        
        # The field 'new_team_name' is not a field in the real post body. 
        # Here we use this for checking whether the team name changed correctly.
        post_res_body_team_list = [
            [
                 # Missing team_id
                {'error_code': ERR_MISSING_REQUIRED_FIELD_CODE}, 
                # Missing team_name
                {'error_code': ERR_MISSING_REQUIRED_FIELD_CODE}, 
                # Missing team_leader_id
                {'error_code': ERR_MISSING_REQUIRED_FIELD_CODE}, 
                # Invalid team_leader_id
                {'error_code': ERR_INTERNAL_ERROR_CODE}, 
                # Invalid team_leader_id
                {'error_code': ERR_LEADER_NOT_A_MEMBER_OF_THE_TEAM_CODE}, 
                # Invalid team_leader_id
                {'error_code': ERR_LEADER_NOT_A_MEMBER_OF_THE_TEAM_CODE}, 
                # Unchanged team_name
                {
                    'error_code': 0, 
                    'new_team_name': self.test_teams[tid_list[0]].name, 
                    'new_team_leader_id': valid_team_leader_id, 
                    'new_team_leader_username': valid_team_leader_user_name, 
                }, 
                # Unchanged team_leader_id
                {
                    'error_code': 0,
                    'new_team_name': valid_team_name, 
                    'new_team_leader_id': -1, 
                    'new_team_leader_username': '', 
                }, 
                # Unchanged team_leader_id
                {
                    'error_code': 0,
                    'new_team_name': valid_team_name, 
                    'new_team_leader_id': -1, 
                    'new_team_leader_username': '', 
                }, 
                # Changed team name and team leader_id
                {
                    'error_code': 0,
                    'new_team_name': valid_team_name, 
                    'new_team_leader_id': valid_team_leader_id, 
                    'new_team_leader_username': valid_team_leader_user_name, 
                }, 
            ], 
            [
                # Missing team_id
                {'error_code': ERR_MISSING_REQUIRED_FIELD_CODE}, 
                # Missing team_name
                {'error_code': ERR_MISSING_REQUIRED_FIELD_CODE}, 
                # Missing team_leader_id
                {'error_code': ERR_MISSING_REQUIRED_FIELD_CODE}, 
                # Invalid team_leader_id
                {'error_code': ERR_INTERNAL_ERROR_CODE}, 
                # Invalid team_leader_id
                {'error_code': ERR_LEADER_NOT_A_MEMBER_OF_THE_TEAM_CODE}, 
                # Invalid team_leader_id
                {'error_code': ERR_LEADER_NOT_A_MEMBER_OF_THE_TEAM_CODE}, 
                # Invalid team_leader_id
                {'error_code': ERR_LEADER_NOT_A_MEMBER_OF_THE_TEAM_CODE},
                # Unchanged team_name
                {
                    'error_code': 0, 
                    'new_team_name': self.test_teams[tid_list[1]].name, 
                    'new_team_leader_id': valid_team_leader_id, 
                    'new_team_leader_username': valid_team_leader_user_name, 
                }, 
                # Unchanged team_leader_id
                {
                    'error_code': 0,
                    'new_team_name': valid_team_name, 
                    'new_team_leader_id': self.test_users[tid_list[1]].id, 
                    'new_team_leader_username': self.test_users[tid_list[1]].username,  
                }, 
                # Unchanged team_leader_id
                {
                    'error_code': 0,
                    'new_team_name': valid_team_name, 
                    'new_team_leader_id': self.test_users[tid_list[1]].id, 
                    'new_team_leader_username': self.test_users[tid_list[1]].username,  
                }, 
                # Changed team name and team leader_id
                {
                    'error_code': 0,
                    'new_team_name': valid_team_name, 
                    'new_team_leader_id': valid_team_leader_id, 
                    'new_team_leader_username': valid_team_leader_user_name, 
                }, 
            ],  
        ]
        
        for uid in uid_list: 
            self.c.login(username=self.test_users[uid].username, password='password')
            # test_teams[0] has all test_users as its members but no lead.
            # test_teams[4] has test_users[2] and test_users[4] as its members and the lead is test_users[2].
            for tid, post_req_body_list, post_res_body_list in zip(tid_list, post_req_body_team_list, post_res_body_team_list):
                
                # POST request
                for req_body, res_body in zip(post_req_body_list, post_res_body_list): 
                    # print(tid, req_body, res_body)
                    old_team_name = self.test_teams[tid].name
                    old_leader_id  = self.test_teams[tid].leader_id
                    
                    resp = self.c.post(reverse('team_view_update'), json.dumps(req_body), content_type="application/json")
                    self.assertEqual(resp.status_code, 200)
                    data = json.loads(resp.content)
                    self.assertEqual(data['error_code'], res_body['error_code'])
                    if res_body['error_code'] == 0: 
                        self.assertEqual(data['new_team_leader_id'], res_body['new_team_leader_id'])
                        self.assertEqual(data['new_team_leader_username'], res_body['new_team_leader_username'])
                        self.assertEqual(Team.query(self.test_teams[tid].id).name, res_body['new_team_name'])
                        
                    # Recover the original record
                    self.test_teams[tid].name = old_team_name
                    self.test_teams[tid].leader_id = old_leader_id
                    self.test_teams[tid].save()
        
    def test_member_edit_team_get_post(self): 
        uid = 2
        tid = uid   # This team is leaded by self.test_users[uid]
        self.c.login(username=self.test_users[uid].username, password='password')
        
        # Get request
        get_req_body_list = [
            # Missing team_id
            {}, 
            {'team_id': self.test_teams[tid].id, }, 
        ]
        
        get_res_code_list = [
            ERR_LACK_OF_AUTHORITY_CODE, 
            ERR_LACK_OF_AUTHORITY_CODE, 
        ]
        
        for req_body, res_code in zip(get_req_body_list, get_res_code_list): 
            resp = self.c.get(reverse('team_view_update'), req_body)
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.content)
            self.assertEqual(data['error_code'], res_code)
            
        # POST request
        post_req_body_list = [
            # Missing some field. But because we first check the authority, so the response should also be str(self.test_teams[tid].id)
            {'team_id': str(self.test_teams[tid].id)}, 
            # A normal request body.
            {'team_id': str(self.test_teams[tid].id), 'team_name': 'abc', 'team_leader_id': self.test_users[uid].id}
        ]
        
        post_res_code_list = [
            ERR_LACK_OF_AUTHORITY_CODE, 
            ERR_LACK_OF_AUTHORITY_CODE, 
        ]
        
        for req_body, res_code in zip(post_req_body_list, post_res_code_list): 
            resp = self.c.post(reverse('team_view_update'), json.dumps(req_body), content_type="application/json")
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.content)
            self.assertEqual(data['error_code'], res_code)

    def test_admin_staff_delete_team(self): 
        uid_list = [0, 0, 1]
        tid_list = [-1, 0, 2]
        req_body_list = [
            # Missing team_id
            {}, 
            {'id': str(self.test_teams[tid_list[1]].id), }, 
            {'id': str(self.test_teams[tid_list[2]].id), }, 
        ]
        
        res_code_list = [
            ERR_MISSING_REQUIRED_FIELD_CODE, 
            0, 
            0, 
        ]
        
        cur_n_teams = self.n_teams
        cur_n_team_members = self.n_team_members
        for uid, tid, req_body, res_code in zip(uid_list, tid_list, req_body_list, res_code_list): 
            self.c.login(username=self.test_users[uid].username, password='password')
            resp = self.c.get(reverse('team_view_delete'), req_body)
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.content)
            self.assertEqual(data['error_code'], res_code)
            if res_code == 0: 
                cur_n_teams -= 1
                cur_n_team_members -= len([x for x in range(2, self.n_users) if tid % x == 0])
                self.assertEqual(Team.objects.all().count(), cur_n_teams)
                with self.assertRaisesMessage(Team.DoesNotExist, 'Team matching query does not exist'):
                    Team.query(self.test_teams[tid].id)
                self.assertEqual(TeamMember.objects.all().count(), cur_n_team_members)
                self.assertEqual(TeamMember.get_team_members(team_id = self.test_teams[tid].id).count(), 0)
                
        
    def test_member_delete_team(self): 
        uid = 2
        tid = 0
        self.c.login(username=self.test_users[uid].username, password='password')
        resp = self.c.get(reverse('team_view_delete'), {'id': self.test_teams[tid].id})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['error_code'], ERR_LACK_OF_AUTHORITY_CODE)
    
class TeamDetailViewTestCase(TestCase): 
    @classmethod
    def setUp(self):
        self.c = Client()
        self.test_users, self.test_teams, self.test_team_members = init_users_and_teams()
        self.n_users = len(self.test_users)
        self.n_teams = len(self.test_teams)
        self.n_team_members = len(self.test_team_members)
        
    def test_detail_view(self): 
        # Admin check team 0 including all usres as members.
        self.c.login(username=self.test_users[0].username, password='password')
        resp = self.c.get(reverse('team_detail', args = [self.test_teams[0].id]))
        self.assertTemplateUsed(resp, 'manage-team/team_detail.html')
        data = resp.context
        self.assertEqual(data["team_id"], self.test_teams[0].id) 
        self.assertEqual(data["team_name"], self.test_teams[0].name)
        self.assertEqual(data["team_leader_id"], -1)
        self.assertEqual(len(data["not_members"]), 0) 
        for i in range(2, self.n_users): 
            self.assertTrue(TeamMember.get_by_team_members(team_id = self.test_teams[0].id, user_id = self.test_users[i].id) in data["members"])
        
        # User 2 check the team 3 (user 2 isn't in the team).   
        self.c.login(username=self.test_users[2].username, password='password')
        resp = self.c.get(reverse('team_detail', args = [self.test_teams[3].id]))
        self.assertRaises(PermissionDenied)

        # User 2 check the team 4 (user 2 is in the team).
        self.c.login(username=self.test_users[2].username, password='password')
        resp = self.c.get(reverse('team_detail', args = [self.test_teams[4].id]))
        data = resp.context
        self.assertEqual(data["team_id"], self.test_teams[4].id) 
        self.assertEqual(data["team_name"], self.test_teams[4].name)
        self.assertEqual(data["team_leader_id"], self.test_users[4].id)
        for i in range(2, self.n_users): 
            if 4 % i == 0:
                self.assertTrue(TeamMember.get_by_team_members(team_id = self.test_teams[4].id, user_id = self.test_users[i].id) in data["members"])
            else:
                self.assertTrue(User.query(self.test_users[i].id) in data["not_members"])
        self.assertEqual(len(data["members"]) + len(data["not_members"]), self.n_users - 2)
        
    def test_admin_staff_leader_add_members(self): 
        tid = 4
        team_id = self.test_teams[tid]
        
        post_req_body_list = [
            # Missing selected_members
            {},       
            # Invalid member
            {'selected_members': [self.test_users[i].id for i in [3, 1]]}, 
            # Valid
            {'selected_members': [self.test_users[i].id for i in[2, 3, 4, 4, 5]]}, 
        ]
        
        post_res_code_list = [
            ERR_MISSING_REQUIRED_FIELD_CODE, 
            ERR_ADD_INVALID_MEMBER_CODE, 
            0, 
        ]
        
        self.c.login(username=self.test_users[0].username, password='password')
        for req_body, res_code in zip(post_req_body_list, post_res_code_list):
            resp = self.c.post(reverse('team_detail_update', args = [self.test_teams[tid].id]), json.dumps(req_body), content_type="application/json")
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.content)
            self.assertEqual(data['error_code'], res_code)
            
        self.assertNotEqual(TeamMember.get_by_team_members(team_id = team_id, user_id = self.test_users[3].id), None)
        self.assertNotEqual(TeamMember.get_by_team_members(team_id = team_id, user_id = self.test_users[5].id), None)
        self.assertEqual(TeamMember.get_team_members(team_id = team_id).count(), 4)
        self.assertEqual(TeamMember.objects.all().count(), self.n_team_members + 2)
        
    def test_member_add_members(self): 
        tid = 4
        self.c.login(username=self.test_users[2].username, password='password')
        team_id = self.test_teams[tid]
        req_body, res_code = {'selected_members': [self.test_users[i].id for i in [2, 3, 4, 4, 5]]}, ERR_LACK_OF_AUTHORITY_CODE
        resp = self.c.post(reverse('team_detail_update', args = [self.test_teams[tid].id]), json.dumps(req_body), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['error_code'], res_code)
    
    def test_admin_staff_delete_members(self): 
        tid = 4
        team_id = self.test_teams[tid].id
        
        get_req_body_list = [
            # Missing selected_members
            {},       
            # Not a member
            {'id': TeamMember.get_by_team_members(team_id = self.test_teams[0].id, user_id = self.test_users[3].id).id}, 
        ]
        
        get_res_code_list = [
            ERR_MISSING_REQUIRED_FIELD_CODE, 
            ERR_NOT_A_MEMBER_OF_THE_TEAM_CODE, 
        ]
        
        self.c.login(username=self.test_users[0].username, password='password')
        for req_body, res_code in zip(get_req_body_list, get_res_code_list):
            resp = self.c.get(reverse('team_detail_delete', args = [team_id]), req_body)
            data = json.loads(resp.content)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data['error_code'], res_code)
            
        # Delete not a leader
        req_body, res_code = {'id': TeamMember.get_by_team_members(team_id = team_id, user_id = self.test_users[2].id).id}, 0
        resp = self.c.get(reverse('team_detail_delete', args = [team_id]), req_body)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['error_code'], res_code)
            
        self.assertEqual(TeamMember.get_by_team_members(team_id = team_id, user_id = self.test_users[2].id), None)
        self.assertEqual(TeamMember.get_team_members(team_id = team_id).count(), 1)
        self.assertEqual(TeamMember.objects.all().count(), self.n_team_members - 1)
        
        # Delete a leader
        req_body, res_code = {'id': TeamMember.get_by_team_members(team_id = team_id, user_id = self.test_users[4].id).id}, 0
        resp = self.c.get(reverse('team_detail_delete', args = [team_id]), req_body)
        data = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['error_code'], res_code)
        
        self.assertEqual(TeamMember.get_by_team_members(team_id = team_id, user_id = self.test_users[4].id), None)
        self.assertEqual(Team.query(self.test_teams[4].id).leader_id, None)
        self.assertEqual(TeamMember.get_team_members(team_id = team_id).count(), 0)
        self.assertEqual(TeamMember.objects.all().count(), self.n_team_members - 2)
        
    def test_leader_delete_members(self): 
        tid = 4
        team_id = self.test_teams[tid]
        
        uid = 4 # leader
        
        post_req_body_list = [
            # Missing selected_members
            {},       
            # Not a member
            {'id': TeamMember.get_by_team_members(team_id = self.test_teams[0].id, user_id = self.test_users[3].id).id}, 
            # Delete himself
            {'id': TeamMember.get_by_team_members(team_id = team_id, user_id = self.test_users[4].id).id}, 
        ]
        
        post_res_code_list = [
            ERR_MISSING_REQUIRED_FIELD_CODE, 
            ERR_NOT_A_MEMBER_OF_THE_TEAM_CODE, 
            ERR_LACK_OF_AUTHORITY_CODE, 
        ]
        
        self.c.login(username=self.test_users[uid].username, password='password')
        for req_body, res_code in zip(post_req_body_list, post_res_code_list):
            resp = self.c.get(reverse('team_detail_delete', args = [self.test_teams[tid].id]), req_body)
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.content)
            self.assertEqual(data['error_code'], res_code)
            
        # Delete not a leader
        req_body, res_code = {'id': TeamMember.get_by_team_members(team_id = self.test_teams[tid].id, user_id =self.test_users[2].id).id}, 0
        resp = self.c.get(reverse('team_detail_delete', args = [self.test_teams[tid].id]), req_body)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['error_code'], res_code)
            
        self.assertEqual(TeamMember.get_by_team_members(team_id = team_id, user_id = self.test_users[2].id), None)
        self.assertEqual(TeamMember.get_team_members(team_id = team_id).count(), 1)
        self.assertEqual(TeamMember.objects.all().count(), self.n_team_members - 1)
    
    def test_member_delete_members(self):
        uid_list = [2, 3, 2]
        tid_list = [4, 3, 4]
        # test_users[2] is a member but not the leader of test_teams[4]
        # So test_users[3] isn't a member in test_teams[4], test_users[2] is a member but not the leader of test_teams[4]
        # They both have no authority to delete members
        team_member = TeamMember.get_by_team_members(team_id = self.test_teams[4].id, user_id = self.test_users[2].id)
        # Get request
        get_req_body_list = [
            # Missing team_id
            {}, 
            # Delete a member not in this team
            {'id': str(team_member.id), }, 
            # Neither admin / staff or the team leader 
            {'id': str(team_member.id), }
        ]
        
        get_res_code_list = [
            ERR_MISSING_REQUIRED_FIELD_CODE, 
            ERR_NOT_A_MEMBER_OF_THE_TEAM_CODE, 
            ERR_LACK_OF_AUTHORITY_CODE, 
        ]
        
        for uid, tid, req_body, res_code in zip(uid_list, tid_list, get_req_body_list, get_res_code_list): 
            self.c.login(username=self.test_users[uid].username, password='password')
            resp = self.c.get(reverse('team_detail_delete', args = [self.test_teams[tid].id]), req_body)
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.content)
            self.assertEqual(data['error_code'], res_code)
        