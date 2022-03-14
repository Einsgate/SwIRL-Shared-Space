from django.db import models
from django.db.models import Q

# Create your models here.

class Reservation(models.Model):
    id = models.IntegerField(primary_key = True)
    title = models.CharField(max_length = 50, default = 'untitled')
    description = models.CharField(max_length = 255, default = '')
    zone_id = models.IntegerField(default = 0)
    zone_name = models.CharField(max_length = 50, default = "noname")
    user_id = models.IntegerField(default = 0)
    team_id = models.IntegerField(default = 0)
    is_long_term = models.BooleanField(default = False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reservation_type = models.IntegerField()
    
    def is_valid(self):
        if self.reservation_type < 0 or self.reservation_type > 2 or not self.start_time or not self.end_time or self.start_time >= self.end_time or self.user_id != 1:
            return False
        else:
            return True
            
    def has_confliction(self):
        # Find all reservations that 
        # start_time < self.end_time AND end_time > self.start_time AND (zone_id = self.zone_id OR reservation_type != self.reservation_type)
        conflict_reservations = Reservation.objects.filter(Q(start_time__lt = self.end_time), Q(end_time__gt = self.start_time), 
            Q(zone_id__exact = self.zone_id) | ~Q(reservation_type = self.reservation_type))
        if len(conflict_reservations) > 0:
            return True
        else:
            return False    
            
    @staticmethod
    def list_all(user_id = 0):
        if user_id == 0:
            return Reservation.objects.all()
        else:
            return Reservation.objects.filter(user_id = user_id)
        
    @staticmethod
    def delete(id = 0):
        Reservation.objects.filter(id = id).delete()
        
    
class User(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    role_id = models.IntegerField()
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 255)
    google_token = models.CharField(max_length = 1000)
    
    
class Role(models.Model):
    id = models.IntegerField(primary_key = True)
    role_name = models.CharField(max_length = 255)
    
class Team(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    leader_id = models.IntegerField()
    
class TeamMembers(models.Model):
    team_id = models.IntegerField()
    user_id = models.IntegerField()
    join_time = models.DateTimeField()
    
class Training(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 1000)
    instructor_id = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    zone_id = models.IntegerField()
    
class TrainingDetail(models.Model):
    training_id = models.IntegerField()
    user_id = models.IntegerField()
    training_result = models.IntegerField()
    registration_time = models.DateTimeField()
    
class Zone(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50, default = "noname")
    is_noisy = models.BooleanField(default = False)
    description = models.CharField(max_length = 500, default = "")
    zone_type = models.IntegerField(default = 1)
    
    @staticmethod
    def list_all():
        return Zone.objects.all().order_by("id")