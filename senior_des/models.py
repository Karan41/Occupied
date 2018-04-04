from django.db import models

# Create your models here.

class Rooms(models.Model):
    room_name = models.CharField(max_length=200)
    room_number = models.CharField(max_length=10)
    is_occupied = models.BooleanField(default = True)

    #prints out the text that wants to be sent
    def __str__(self):
        if self.is_occupied:
            return self.room_name + ", room number " + str(self.room_number) + " is occupied "  
        else:
            return self.room_name + ", room number " + str(self.room_number) + " is not occupied "

    #returns is occupied if true and is not occupied if false
    #doesn't work just reemplimented self
    def is_room_occupied(self):
        if self.is_occupied:
            return "occupied"
        else:
            return "not occupied"

    def room_arr(self):
        if self.is_occupied:
            return True
        else:
            return False
