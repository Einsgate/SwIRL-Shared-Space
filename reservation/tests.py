from django.test import TestCase
from .models import Reservation

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