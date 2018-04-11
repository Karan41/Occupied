from django.shortcuts import render, HttpResponse

from senior_des.models import Rooms, RoomTimes
import datetime
import pytz
from faker import Faker
# Create your views here.
fake = Faker()

def room(request):
    rooms = Rooms.objects.all()
    for room in rooms:
        #print(room);
        room.text = room
        temp = str(room)
        #print("HIIII ", type(temp))
        if "not" not in temp:
            room.isOcc = False
        else:
            room.isOcc = True
        #print(room)

    #print(type(rooms))
    args = {'rooms' : rooms}
    return render(request, 'senior_des/room.html', args)

def avai_room(request):
    rooms = Rooms.objects.all()
    for room in rooms:
        #print(room);
        room.text = room
        temp = str(room)
        #print("HIIII ", type(temp))
        if "not" not in temp:
            room.isOcc = False
        else:
            room.isOcc = True
        #print(room)

    #print(type(rooms))
    args = {'rooms' : rooms}
    return render(request, 'senior_des/avai_room.html', args)

def home(request):
    return render(request, 'senior_des/homepage/startbootstrap-agency-master/index.html')

def database(request):
    #add to database the request sent
    print('WHATS GOING ON:  ', request)
    local_tz = pytz.timezone('America/Chicago')
    localtimestamp = datetime.datetime.now().replace(tzinfo=pytz.utc).astimezone(local_tz).strftime('%H:%M')
    timeAMPM = datetime.datetime.now().replace(tzinfo=pytz.utc).astimezone(local_tz).strftime("%I:%M %p")
    #### COMMENT OUT FAKE TIME
    localtimestamp = fake.time(pattern="%H:%M", end_datetime=None)
    s = request.META['QUERY_STRING']


    print(s)
    each_info = s.split('+')
    error_message = {}
    if (each_info[0] != 'b9c4t5tac1') :
       error_message = 'BAD USER (in future should lock this user out of website for 5 min)'
       args = {'message' : error_message}
       return render(request, 'senior_des/error.html', args)
    elif (len(each_info) != 3):
        print("how many splits: ", each_info)
        error_message ['message'] = 'not enough input parameters. Should be ?Password+room_name+is_occupied'
        args = {'message' : error_message}
        return render(request, 'senior_des/error.html', args)

    if (each_info[2] == 'false'):
        each_info[2] = False
    elif (each_info[2] == 'true'):
        each_info[2] = True
    else:
        error_message ['message'] = 'is_occupied is not the right value: enter false or true for it'
        args = {'message' : error_message}
        return render(request, 'senior_des/error.html', args)



    x = Rooms (name=str(each_info[1]), timestamp = timeAMPM, is_occupied=bool(each_info[2]))
    roomTime = RoomTimes(room=str(each_info[1]), time = localtimestamp, occupied=bool(each_info[2]))
    roomTime.save()
    print("ROOMTIMES TABLE: ", RoomTimes.objects.all())
    r = Rooms.objects.all().filter(name=each_info[1])

    print (type(Rooms.objects.all()))
    if(len(r) == 0):
        x.save()
        print("Room doesn't exist")
        #if room does exist then update the state
    else:
        o = r.first()
        print("here is the room being updated: ", o)
        o.is_occupied = x.is_occupied
        o.timestamp = x.timestamp
        o.save()
    error_message = 'successful room change: updated room ', each_info[1], ' with room number of ',each_info[2]
    print (error_message , ' TESTINGGGGG')
    args = {'message' : error_message}
    return render(request, 'senior_des/error.html', args)

def refresh(request):

    s = request.META['QUERY_STRING']


    print(s)
    each_info = s.split('+')
    error_message = {}
    if (each_info[0] != 'b9c4t5tac1') :
       error_message = 'BAD USER (in future should lock this user out of website for 5 min)'
       args = {'message' : error_message}
       return render(request, 'senior_des/error.html', args)

    for room in Rooms.objects.all():
        room.delete()
    rooms = Rooms.objects.all()
    for room in rooms:
        #print(room);
        room.text = room
        temp = str(room)
        #print("HIIII ", type(temp))
        if "not" not in temp:
            room.isOcc = False
        else:
            room.isOcc = True
        #print(room)

    #print(type(rooms))
    args = {'rooms' : rooms}
    return render(request, 'senior_des/error.html', args)
