from django.db import models

# Create your models here.

class Rooms(models.Model):
    name = models.CharField(max_length=200)
    timestamp = models.CharField(max_length=10)
    is_occupied = models.BooleanField(default = True)

    #prints out the text that wants to be sent
    def __str__(self):
        if self.is_occupied:
            return self.name + ", is occupied at time: " + str(self.timestamp)
        else:
            return self.name + ", is empty at time: " + str(self.timestamp)

    #returns is occupied if true and is not occupied if false
    #doesn't work just reemplimented self
    def is_room_occupied(self):
        if self.is_occupied:
            return "occupied"
        else:
            return "empty"

    def room_arr(self):
        if self.is_occupied:
            return True
        else:
            return False

class RoomTimes(models.Model):
    room = models.CharField(max_length=200)
    time = models.CharField(max_length=10)
    occupied = models.BooleanField(default = True)
