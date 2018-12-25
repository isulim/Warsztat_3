from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=32)
    seats = models.SmallIntegerField()
    projector = models.BooleanField()
    floor = models.SmallIntegerField(null=True)
    desks = models.BooleanField(default=True)


class Reservation(models.Model):
    owner = models.CharField(max_length=32)
    comment = models.CharField(max_length=128, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
