from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=32)
    seats = models.SmallIntegerField()
    projector = models.BooleanField()
    floor = models.SmallIntegerField(null=True)
    desks = models.BooleanField(default=True)
