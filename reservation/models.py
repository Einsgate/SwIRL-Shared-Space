from django.db import models

# Create your models here.

class Reservation(models.Model):
    id = models.IntegerField(primary_key = True)
    zone_id = models.IntegerField()
    user_id = models.IntegerField()
    team_id = models.IntegerField()
    is_long_term = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reservation_type = models.IntegerField()
    
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
    is_noisy = models.IntegerField()
    description = models.CharField(max_length = 1000)
    zone_type = models.IntegerField()
    