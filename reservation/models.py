from django.db import models
from django.db.models import Q, Count
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from .const import *
from allauth.account.views import email

# Create your models here.

class Reservation(models.Model):
    #id = models.IntegerField(primary_key = True, blank=True)
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
        if self.reservation_type <= 0 or self.reservation_type > 3 or not self.start_time or not self.end_time or self.start_time >= self.end_time or self.user_id != 1:
            return False
        else:
            return True
            
    def has_confliction(self):
        # Find all reservations that 
        # start_time < self.end_time AND end_time > self.start_time AND zone_id = self.zone_id 
        conflict_reservations = Reservation.objects.filter(Q(start_time__lt = self.end_time), Q(end_time__gt = self.start_time), 
            Q(zone_id__exact = self.zone_id))
        conflict = len(conflict_reservations) > 0
            
        # For those reservations that break the quietness requirement, return a warning back
        if self.reservation_type == RESV_TYPE_REQ_QUIET: # Only check when the reservation require a quiet environment
            # Query those overlapped noisy reservations
            conflict_on_quiet_reservations = Reservation.objects.filter(Q(start_time__lt = self.end_time), Q(end_time__gt = self.start_time), 
                Q(reservation_type__exact = RESV_TYPE_NOISY))
            warning = len(conflict_on_quiet_reservations) > 0
        else:
            warning = False
        
        return conflict, warning  
            
    @staticmethod
    def list_all(user_id = 0):
        if user_id == 0:
            return Reservation.objects.all()
        else:
            return Reservation.objects.filter(user_id = user_id)
        
    @staticmethod
    def delete(id = 0):
        Reservation.objects.filter(id = id).delete()

class Role(models.Model):
    role_name = models.CharField(max_length = 255)

    @staticmethod
    def findById(id = 0):
        return Role.objects.filter(id = id).first()

class User(AbstractUser):
    #role_id = models.IntegerField(default = 3)
    role_id = models.ForeignKey('Role', on_delete = models.CASCADE, default = 3)
    
    #google_token = models.CharField(max_length = 1000)
    #last_login = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='last_login_time')

    # @staticmethod
    # def findUserByName(username=0, password=0):
    #     user_list = User.objects.filter(username = username, password = password)
    #     if len(user_list) == 1:
    #         return user_list.first()
    @staticmethod
    def list_all(role_id=0):
        return User.objects.filter(~Q(role_id=ROLE_ADMIN)).order_by("-id")
    @staticmethod
    def list_staff(role_id=0):
        return User.objects.filter(role_id = role_id)
    @staticmethod
    def delete(id = 0):
        user = User.objects.filter(id = id).delete()
    @staticmethod
    def findUserById(id = 0):
        return User.objects.filter(id = id).first()
    @staticmethod
    def findListByEmail(email):
        return User.objects.filter(email = email)
        
    @staticmethod
    def list_not_admin_staff(): 
        return User.objects.exclude(role_id__in=[ROLE_ADMIN, ROLE_STAFF])

    @staticmethod
    def list_not_members(team_id):
        return User.objects.exclude(role_id__in=[ROLE_ADMIN, ROLE_STAFF]).exclude(pk__in=TeamMember.get_team_members(team_id).values_list('user_id', flat=True))
        
    @staticmethod
    def query(user_id):
        return User.objects.get(pk = user_id)
    
class Team(models.Model):
    name = models.CharField(max_length = 50)
    leader_id = models.ForeignKey('User', on_delete = models.SET_NULL, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add = True)
    
    # Return teams whose leader is user_id
    @staticmethod
    def list_all(user_id = 0):
        if user_id == 0:
            return Team.objects.all().annotate(num_teammembers = Count('teammember'))
        else:
            # Return the teams that user_id is in
            # SELECT team.* 
            # FROM team INNER JOIN team_members
            # ON team.id = team_members.user_id
            # WHERE team_members.user_id = user_id
            return Team.objects.annotate(num_teammembers = Count('teammember')).filter(teammember__user_id__exact = user_id)
        
    @staticmethod
    def query(team_id):
        return Team.objects.get(pk = team_id)
        
    @staticmethod
    def delete(id = 0):
        Team.objects.filter(id = id).delete()
    
class TeamMember(models.Model):
    team_id = models.ForeignKey('Team', on_delete = models.CASCADE)
    user_id = models.ForeignKey('User', on_delete = models.CASCADE)
    join_time = models.DateTimeField(auto_now_add=True)
    
    @staticmethod
    def query(member_id):
        return TeamMember.objects.get(pk = member_id);
    @staticmethod
    def get_team_members(team_id):
        return TeamMember.objects.filter(team_id = team_id)
    @staticmethod
    def get_by_team_members(team_id, user_id):
        return TeamMember.objects.filter(team_id = team_id, user_id = user_id).first()

class Training(models.Model):
    #id = models.IntegerField(primary_key = True, blank=True)
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 1000, default = '')
    instructor_id = models.IntegerField(default = 0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    #0: not start, 1: processing, 2: finished, 3: graded
    training_status = models.IntegerField(default = 0)
    zone_id = models.IntegerField()

    @staticmethod
    def list_all(user_id = 0):
        if user_id == 0:
            return Training.objects.all()
        else:
            return Training.objects.filter(user_id = user_id)

    @staticmethod
    def findById(id):
        return Training.objects.filter(id=id).first()

    @staticmethod
    def list_exception(oldIds):
        return Training.objects.filter(training_status=0).filter(~Q(id__in=oldIds))

    @staticmethod
    def findListByName(name):
        return Training.objects.filter(name = name, training_status=0)

    @staticmethod
    def delete(id = 0):
        Training.objects.filter(id = id).delete()

# this is for change the training results like team details    
class TrainingDetail(models.Model):
    #id = models.IntegerField(primary_key = True, blank=True)
    user_id = models.ForeignKey('User', on_delete = models.CASCADE)
    training_id = models.ForeignKey('Training', on_delete = models.CASCADE)
    registration_time = models.DateTimeField(auto_now_add=True)
    #0: not start, 1: processing, 2: finished, 3: graded
    training_status = models.IntegerField(default = 0)
    #0: not graded, 1: failed, 2: passed
    training_result = models.IntegerField(default = 0)

    @staticmethod
    def list_all(user_id = 0):
        return TrainingDetail.objects.filter(user_id = user_id)

    @staticmethod
    def listByTrainingId(training_id):
        return TrainingDetail.objects.filter(training_id = training_id)

    @staticmethod
    def findById(id):
        return TrainingDetail.objects.filter(id = id).first()

    @staticmethod
    def list_exception(user_id = 0):
        if user_id == 0:
            return TrainingDetail.objects.all()
        else:
            return TrainingDetail.objects.filter(user_id = user_id)

    @staticmethod
    def delete(id = 0):
        TrainingDetail.objects.filter(id = id).delete()

class Zone(models.Model):
    #id = models.IntegerField(primary_key = True, blank=True)
    name = models.CharField(max_length = 50, default = "noname")
    is_noisy = models.BooleanField(default = False)
    description = models.CharField(max_length = 500, default = "")
    zone_type = models.IntegerField(default = 1)
    
    @staticmethod
    def list_all():
        return Zone.objects.all().order_by("id")