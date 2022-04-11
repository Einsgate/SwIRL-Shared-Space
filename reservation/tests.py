from django.test import TestCase
from .models import *

from django.test import Client
import json
from dateutil import parser
from pytz import timezone

from .const import *
from .errors import *
import numpy as np
import random

from django.urls import reverse

# Create your tests here.

# Test modals
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
        
        # self.assertEqual(resp.status_code, 200)
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
        
        # self.assertEqual(resp.status_code, 200)
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
        
        # self.assertEqual(resp.status_code, 200)
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
            'user_id': 1,
            
        }), content_type="application/json")
        
        # self.assertEqual(resp.status_code, 200)
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
        # self.assertEqual(resp.status_code, 200)
        print(resp.content)
        data = json.loads(resp.content)
        self.assertEqual(data["error_code"], 0)  # error_code = 0
        
        # Check if it is deleted
        self.assertEqual(len(Reservation.objects.filter(id=id)), 0)

    def test_zone_list(self):
        self.c.login(username='admin', password='admin')
        resp = self.c.get('/zone/list')
        self.assertEqual(resp.status_code, 200)
        
        data = json.loads(resp.content)
        self.assertEqual(data["error_code"], 0)  


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
    
    num_users = 6
    num_teams = 5
    
    role_admin = Role.objects.get(id = ROLE_ADMIN)
    role_staff = Role.objects.get(id = ROLE_STAFF)
    role_team_leader = Role.objects.get(id = ROLE_LEAD, role_name = "team leader")
    role_member = Role.objects.get(id = ROLE_MEMBER, role_name = "member")

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
        x = random.randint(1, self.n_teams)
        tid = self.test_teams[x].id
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
            
            self.assertEqual(resp.context['team_list_title'], 'Team List')
        
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
        post_body_list = [
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
        
        response_list = [
            ERR_MISSING_REQUIRED_FIELD_CODE, 
            ERR_MISSING_REQUIRED_FIELD_CODE, 
            ERR_MISSING_TEAM_NAME_CODE, 
            ERR_MISSING_TEAM_LEADER_CODE, 
            ERR_ADMIN_STAFF_TEAM_LEADER_CODE, 
            ERR_ADMIN_STAFF_TEAM_LEADER_CODE, 
        ]
            
        for username in [self.test_users[0].username, self.test_users[1].username]:
            self.c.login(username=username, password='password')
        
            for post_body, response in zip(post_body_list, response_list):
                resp = self.c.post(reverse('team_view_create'), json.dumps(post_body), content_type="application/json")
                self.assertEqual(resp.status_code, 200)
                
                data = json.loads(resp.content)
                # print(data['error_msg'])
                self.assertEqual(data['error_code'], response)
                
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
        
    def test_admin_staff_edit_team(self): 
        # team_index = 2
        # valid_team_id = self.test_teams[team_index].id
        # valid_team_name = 'abc'
        # valid_team_leader_id = self.test_members[3].id
        # payload_list = [
        #     # Missing the team_name
        #     {'team_id': valid_team_id, 'team_name': '', 'team_leader_id': valid_team_leader_id},       
        #     # Missing the leader_id
        #     {'team_id': valid_team_id, 'team_name': valid_team_name: 'team_leader_id', ''},   
        # ]
        
        # response_list = [
        #     {'team_name': self.test_teams[team_index].name, 'team_leader_id': valid_team_id
            
        # ]
        pass
        
    def test_member_edit_team(self): 
        uid = 2
        tid = 0
        self.c.login(username=self.test_users[uid].username, password='password')
        resp = self.c.post(reverse('team_view_update'), json.dumps({
            'team_id': self.test_teams[tid].id, 'team_name': 'abc', 'team_leader_id': self.test_users[uid].id
        }), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['error_code'], ERR_LACK_OF_AUTHORITY_CODE)

    def test_admin_staff_delete_team(self): 
        pass
        
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
        
    def test_admin_staff_leader_add_members(self): 
        pass
        
    def test_member_add_members(self): 
        pass
    
    def test_admin_staff_delete_members(self): 
        pass
        
    def test_leader_delete_members(self): 
        pass
    
    def test_member_delete_members(self):
        pass
        