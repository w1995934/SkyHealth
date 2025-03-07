from django.db import models

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

class DepartmentLeader(models.Model):
    fName = models.CharField(max_length=NAMELENGTH)
    lName = models.CharField(max_length=NAMELENGTH)
    email = models.EmailField(unique=UNIQUE)
    username = models.CharField(max_length=NAMELENGTH, unique=UNIQUE)
    password = models.CharField(max_length=PASSWORDLENGTH)
    depID = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.fName} {self.lName}"

class DepartmentSummary(models.Model):
    dsSummary = models.TextField()
    date = models.DateField(auto_now_add=True)
    depID = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Summary for Department {self.depID} on {self.date}"

class Team(models.Model):
    teamName = models.CharField(max_length=TITLELENGTH)
    depID = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.teamName

class Engineer(models.Model):
    fName = models.CharField(max_length=NAMELENGTH)
    lName = models.CharField(max_length=NAMELENGTH)
    email = models.EmailField(unique=UNIQUE)
    username = models.CharField(max_length=NAMELENGTH, unique=UNIQUE)
    password = models.CharField(max_length=PASSWORDLENGTH)
    teamID = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.fName} {self.lName}"

class TeamLeader(models.Model):
    fName = models.CharField(max_length=NAMELENGTH)
    lName = models.CharField(max_length=NAMELENGTH)
    email = models.EmailField(unique=UNIQUE)
    username = models.CharField(max_length=NAMELENGTH, unique=UNIQUE)
    password = models.CharField(max_length=PASSWORDLENGTH)
    teamID = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.fName} {self.lName}"

class TeamSummary(models.Model):
    tsSummary = models.TextField()
    date = models.DateField(auto_now_add=True)
    teamID = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Summary for Team {self.teamID} on {self.date}"

class SeniorManager(models.Model):
    fName = models.CharField(max_length=NAMELENGTH)
    lName = models.CharField(max_length=NAMELENGTH)
    email = models.EmailField(unique=UNIQUE)
    username = models.CharField(max_length=NAMELENGTH, unique=UNIQUE)
    password = models.CharField(max_length=PASSWORDLENGTH)

    def __str__(self):
        return f"{self.fName} {self.lName}"

class Review(models.Model):
    answer = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    cardID = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True)
    engineID = models.ForeignKey(Engineer, on_delete=models.SET_NULL, null=True)
    teamLeadID = models.ForeignKey(TeamLeader, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Review for Card {self.cardID} by Engineer {self.engineID}"