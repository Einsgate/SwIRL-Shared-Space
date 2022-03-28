from django.test import TestCase
from .models import *

from django.test import Client
import json
from dateutil import parser
from pytz import timezone
# Create your tests here.


class ReservationTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        
        #Reservation.objects.create(title = 'setup1', reservation_type = 0, start_time = '2000-01-01 12:00:00', end_time = '2000-01-01 12:30:00', user_id = 1)

    def test_is_valid(self):
        reservation1 = Reservation(title = 'test', reservation_type = 0, start_time = '2022-01-01 13:00:00',
            end_time = '2022-01-01 14:00:00', user_id = 1)
        reservation2 = Reservation(title = 'test', reservation_type = 3, start_time = '2022-01-01 13:00:00',
            end_time = '2022-01-01 14:00:00', user_id = 1)
        reservation3 = Reservation(title = 'test', reservation_type = 0, start_time = '2022-01-01 15:00:00',
            end_time = '2022-01-01 14:00:00', user_id = 1)
        
        self.assertEqual(reservation1.is_valid(), True)
        self.assertEqual(reservation2.is_valid(), False)
        self.assertEqual(reservation3.is_valid(), False)
        
        
    def test_has_confliction(self):
        Reservation.objects.create(zone_id = 1, reservation_type = 1, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00', user_id = 1)
        Reservation.objects.create(zone_id = 2, reservation_type = 0, start_time = '2000-01-02 12:00:00', end_time = '2000-01-02 12:30:00', user_id = 1)
        
        self.assertEqual(Reservation(zone_id = 1, reservation_type = 1, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00', user_id = 1).has_confliction(), True)
        self.assertEqual(Reservation(zone_id = 3, reservation_type = 1, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00', user_id = 1).has_confliction(), False)
        self.assertEqual(Reservation(zone_id = 3, reservation_type = 0, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00', user_id = 1).has_confliction(), True)
        self.assertEqual(Reservation(zone_id = 3, reservation_type = 2, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00', user_id = 1).has_confliction(), True)

        
        #response = c.post('/reservation/create', {'title': "test", "reservation_type": 0, start_time = 'xxx', end_time = "xxx"})
        
    def test_create_success(self):
        resp = self.c.post('/reservation/create', json.dumps({
            'title': 'test', 
            'reservation_type': 0, 
            'is_long_term': False,
            'zone_id': 1, 
            'zone_name': 'zone 1', 
            'start_time': '2022-03-14 12:00:00', 
            'end_time': '2022-03-14 13:00:00', 
            'user_id': 1,
            
        }), content_type="application/json")
        
        self.assertEqual(resp.status_code, 200)
        print(resp.content)
        data = json.loads(resp.content)
        self.assertEqual(data["error_code"], 0)
        
       
    def test_create_fail(self):
        resp = self.c.post('/reservation/create', json.dumps({
            'title': 'test', 
            'reservation_type': 0, 
            'is_long_term': False,
            'zone_id': 1, 
            'zone_name': 'zone 1', 
            'start_time': '2022-03-14 12:00:00', 
            'end_time': '2022-03-14 13:00:00', 
            'user_id': 1,
            
        }), content_type="application/json")
        
        self.assertEqual(resp.status_code, 200)
        print(resp.content)
        data = json.loads(resp.content)
        self.assertEqual(data["error_code"], 0)
        
        
        
        # Since this reservation is conflicted with the previous one, it should fail
        resp = self.c.post('/reservation/create', json.dumps({
            'title': 'test', 
            'reservation_type': 0, 
            'is_long_term': False,
            'zone_id': 1, 
            'zone_name': 'zone 1', 
            'start_time': '2022-03-14 12:00:00', 
            'end_time': '2022-03-14 14:00:00', 
            'user_id': 1,
            
        }), content_type="application/json")
        
        self.assertEqual(resp.status_code, 200)
        print(resp.content)
        data = json.loads(resp.content)
        self.assertNotEqual(data["error_code"], 0)  # Should fail (ereor_code != 0)
    
        # Fail since missing required field
        resp = self.c.post('/reservation/create', json.dumps({
            'title': 'test', 
            'reservation_type': 0, 
            'is_long_term': False,
            'zone_name': 'zone 1', 
            'start_time': '2022-03-14 12:00:00', 
            'end_time': '2022-03-14 14:00:00', 
            'user_id': 1,
            
        }), content_type="application/json")
        
        self.assertEqual(resp.status_code, 200)
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
            'user_id': 1,
            
        }), content_type="application/json")
        
        self.assertEqual(resp.status_code, 200)
        print(resp.content)
        data = json.loads(resp.content)
        self.assertNotEqual(data["error_code"], 0)  # Should fail (ereor_code != 0)
    
    def test_list(self):
        Reservation.objects.all().delete()
        reservations = [
            Reservation(zone_id = 1, reservation_type = 1, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00', user_id = 1),
            Reservation(zone_id = 2, reservation_type = 0, start_time = '2000-01-02 12:00:00', end_time = '2000-01-02 12:30:00', user_id = 1),
            Reservation(zone_id = 3, reservation_type = 2, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00', user_id = 1),
            Reservation(zone_id = 4, reservation_type = 1, start_time = '2000-01-02 12:00:00', end_time = '2000-01-02 12:30:00', user_id = 1),
        ]

        for r in reservations:
            r.save()
        
        resp = self.c.get('/reservation/list')
        
        self.assertEqual(resp.status_code, 200)
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
            self.assertEqual(r["user_id"], reservations[i].user_id) 
        
    def test_delete(self):
        Reservation.objects.all().delete()
        reservations = [
            Reservation(zone_id = 1, reservation_type = 1, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00', user_id = 1),
            Reservation(zone_id = 2, reservation_type = 0, start_time = '2000-01-02 12:00:00', end_time = '2000-01-02 12:30:00', user_id = 1),
            Reservation(zone_id = 3, reservation_type = 2, start_time = '2000-01-03 12:00:00', end_time = '2000-01-03 12:30:00', user_id = 1),
            Reservation(zone_id = 4, reservation_type = 1, start_time = '2000-01-02 12:00:00', end_time = '2000-01-02 12:30:00', user_id = 1),
        ]
        
        id = 0
        for r in reservations:
            r.save()
            id = r.id
            
        self.assertEqual(len(Reservation.objects.filter(id=id)), 1)
        
        # Delete reservation with the given id
        resp = self.c.get('/reservation/delete', {'id': id})
        self.assertEqual(resp.status_code, 200)
        print(resp.content)
        data = json.loads(resp.content)
        self.assertEqual(data["error_code"], 0)  # error_code = 0
        
        # Check if it is deleted
        self.assertEqual(len(Reservation.objects.filter(id=id)), 0)

    def test_zone_list(self):
        resp = self.c.get('/zone/list')
        self.assertEqual(resp.status_code, 200)
        
        data = json.loads(resp.content)
        self.assertEqual(data["error_code"], 0)  


class TeamTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        
        role_admin = Role.objects.get(id = 0)
        role_staff = Role.objects.get(id = 1)
        role_team_leader = Role.objects.get(id = 2)
        role_member = Role.objects.get(id = 3)
        
        # Test data
        # Default admin
        # superuser = User(username = 'admin', email = 'admin@admin.net', is_active = True, is_superuser = True, is_staff = True, role_id = role_admin)
        # superuser.set_password('admin')
        # superuser.save()
        
        # test_member_1 = User(username = 'test_member_1', email = 'test_member_1@tamu.edu', is_active = True, is_superuser = True, is_staff = True, role_id = role_member)
        # test_member_1.set_password('123')
        # test_member_1.save()
        
        # test_member_2 = User(username = 'test_member_2', email = 'test_member_2@tamu.edu', is_active = True, is_superuser = True, is_staff = True, role_id = role_member)
        # test_member_2.set_password('123')
        # test_member_2.save()
        
        # #UserModel = apps.get_model('reservation', 'User')
        # User.objects.create(username = "test_admin_1", email = "test_admin_1@tamu.edu", role_id = role_admin)
        # User.objects.create(username = "test_admin_2", email = "test_admin_2@tamu.edu", role_id = role_admin)
        # User.objects.create(username = "test_staff_1", email = "test_staff_1@tamu.edu", role_id = role_staff)
        # User.objects.create(username = "test_staff_2", email = "test_staff_2@tamu.edu", role_id = role_staff)
        #User.objects.create(id = 3, username = "test_lead_1", email = "test_lead_1@tamu.edu", role_id = 2)
        #User.objects.create(id = 3, username = "test_lead_2", email = "test_lead_2@tamu.edu", role_id = 2)
        #user5 = UserModel.objects.create(username = "test_member_1", email = "test_member_1@tamu.edu", role_id = 2)
        self.test_member_1 = User.objects.get(username = "test_member_1")
        # test_member_2 = User.objects.get(username = "test_member_2")
        # test_member_3 = User.objects.create(username = "test_member_3", email = "test_member_3@tamu.edu", role_id = role_member)
        # User.objects.create(username = "test_member_4", email = "test_member_4@tamu.edu", role_id = role_member)
        # User.objects.create(username = "test_member_5", email = "test_member_5@tamu.edu", role_id = role_member)
    
    
       # Team = apps.get_model('reservation', 'Team')
        self.team1 = Team.objects.get(name = "test_team_1")
        self.team2 = Team.objects.get(name = "test_team_2")
        
        #TeamMember = apps.get_model('reservation', 'TeamMember')
        # TeamMember.objects.create(team_id = team1, user_id = test_member_1)
        # TeamMember.objects.create(team_id = team1, user_id = test_member_2)
        # TeamMember.objects.create(team_id = team1, user_id = test_member_3)

        
    def test_list(self):
        user_id = self.test_member_1.id
        self.assertEqual(len(Team.list_all()), 2)
        self.assertEqual(len(Team.list_all(user_id = user_id)), 1)
        
       # self.c.request.user = User.objects.get(id = 1)
        #self.c.user = User.objects.get(username = "test_admin_1")
        self.c.login(username='admin', password='admin')
        
        resp = self.c.get('/team/view')
        self.assertEqual(resp.status_code, 200)
        
        teams = resp.context['teams']
        self.assertEqual(len(teams), 2)
        
    def test_delete_team(self):
        deleted_team_id = self.team2.id
        # Team.delete(id = deleted_team_id)
        # self.assertEqual(len(Team.objects.filter(id = deleted_team_id)), 0)
        
        self.c.login(username='admin', password='admin')
        resp = self.c.get('/team/delete?team_id={deleted_team_id}'.format(deleted_team_id = deleted_team_id))
        self.assertEqual(resp.status_code, 200)
        
        
    def test_list_team_members(self):
        team_id = self.team1.id
        members = TeamMember.get_team_members(team_id = team_id)
        self.assertEqual(len(members), 3)
        
    def test_team_create(self):
        resp = self.c.post('/team/create', json.dumps({
            'name': 'test_team_create', 
        }), content_type="application/json")
        
        self.assertEqual(resp.status_code, 200)
        print(resp.content)
        data = json.loads(resp.content)
        self.assertEqual(data["error_code"], 0)