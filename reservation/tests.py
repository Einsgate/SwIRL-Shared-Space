from django.test import TestCase
from .models import Reservation

from django.test import Client
# Create your tests here.


class ReservationTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        
        Reservation.objects.create(title = 'setup1', reservation_type = 0, start_time = '2000-01-01 12:00:00', end_time = '2000-01-01 12:30:00', user_id = 1)

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
        
    # def test_delete(self):
        # response = c.post('/reservation/create', {'title': "test", "reservation_type": 0, start_time = 'xxx', end_time = "xxx"})
        
        # id = response.id
        
        # response = c.get('/reservation/delete', {'id': id})
        # self.assertEqual(response.error_code, 0)
        
        # r = Reservation.objects.filter(id = 0)
        # self.assertIsNone(r)
