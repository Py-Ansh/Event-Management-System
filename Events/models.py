from django.db import models


# Create your models here.


class Event(models.Model):

    eventID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    desc = models.TextField()
    cost = models.IntegerField()
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    completed = models.BooleanField(default=0)

    number_of_participants = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.eventID}"
    

class Participants(models.Model):
    sno = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    eventID = models.CharField(max_length=10)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username} - {self.eventID}"
    