from django.test import TestCase
from .models import Reservation

from django.test import Client
# Create your tests here.


class ReservationTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def test_is_valid(self):
        
        
        
        reservation1 = Reservation(title = 'test', reservation_type = 0, start_time = '2022-01-01 13:00:00',
            end_time = '2022-01-01 14:00:00', user_id = 1)
        reservation2 = Reservation(title = 'test', reservation_type = -1, start_time = '2022-01-01 13:00:00',
            end_time = '2022-01-01 14:00:00', user_id = 1)
        reservation3 = Reservation(title = 'test', reservation_type = 0, start_time = '2022-01-01 15:00:00',
            end_time = '2022-01-01 14:00:00', user_id = 1)
        
        self.assertEqual(reservation1.is_valid(), True)
        self.assertEqual(reservation2.is_valid(), True)
        self.assertEqual(reservation3.is_valid(), False)
        
        
    # def test_delete(self):
        # response = c.post('/reservation/create', {'title': "test", "reservation_type": 0, start_time = 'xxx', end_time = "xxx"})
        
        # id = response.id
        
        # response = c.get('/reservation/delete', {'id': id})
        # self.assertEqual(response.error_code, 0)
        
        # r = Reservation.objects.filter(id = 0)
        # self.assertIsNone(r)
