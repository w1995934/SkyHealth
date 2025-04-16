from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

TITLELENGTH = 200
PASSWORDLENGTH = 64
NAMELENGTH = 50
UNIQUE = True


class Card(models.Model):
    cardTitle = models.CharField(max_length=TITLELENGTH)
    cardDetail = models.TextField()

    def __str__(self):
        return self.cardTitle


class Department(models.Model):
    depName = models.CharField(max_length=TITLELENGTH, unique=UNIQUE)

    def __str__(self):
        return self.depName


class DepartmentSummary(models.Model):
    dsSummary = models.TextField()
    date = models.DateField(auto_now_add=True)
    depID = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Summary for Department {self.depID} on {self.date}"


class Team(models.Model):
    teamName = models.CharField(max_length=TITLELENGTH)
    depID = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.teamName


class TeamSummary(models.Model):
    tsSummary = models.TextField()
    date = models.DateField(auto_now_add=True)
    teamID = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Summary for Team {self.teamID} on {self.date}"


class Profile(models.Model):
    ROLE_CHOICES = [
        ('ENGINEER', 'Engineer'),
        ('TEAM_LEADER', 'Team Leader'),
        ('DEPARTMENT_LEADER', 'Department Leader'),
        ('SENIOR_MANAGER', 'Senior Manager'),
        ('SERVER_ADMIN', 'Server Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    teamID = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True)
    depID = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Review(models.Model):
    answer = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    cardID = models.ForeignKey('Card', on_delete=models.SET_NULL, null=True)
    userID = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Review for Card {self.cardID} by User {self.userID}"