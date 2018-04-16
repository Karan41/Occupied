from django.shortcuts import render, HttpResponse
from django.db.models import Count, Q
from collections import defaultdict

from senior_des.models import Rooms, RoomTimes
import datetime
import pytz
from faker import Faker
import json
# Create your views here.

class RoomInfo:
    def __init__(self, timeRangeMap):
        self.timeRangeMap = defaultdict(lambda: 0)

fake = Faker()

def room(request):
    rooms = Rooms.objects.all()
    for room in rooms:
        #print(room);
        room.text = room
        temp = str(room)
        #print("HIIII ", type(temp))
        if "empty" not in temp:
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
        if "empty" not in temp:
            room.isOcc = False
        else:
            room.isOcc = True
        #print(room)

    #print(type(rooms))
    args = {'rooms' : rooms}
    return render(request, 'senior_des/avai_room.html', args)

def home(request):
    rooms = Rooms.objects.all()
    for room in rooms:
        #print(room);
        room.text = room
        temp = str(room)
        #print("HIIII ", type(temp))
        if "empty" not in temp:
            room.isOcc = False
        else:
            room.isOcc = True
        #print(room)

    #print(type(rooms))
    args = {'rooms' : rooms, 'length' : rooms.count()}
    return render(request, 'senior_des/homepage/startbootstrap-agency-master/index.html', args)

def time_graphs(request):

    data = RoomTimes.objects \
        .values('room') \
        .annotate(occupied=Count('time', filter=Q(occupied=True))) \
        .order_by('time')

    dataTime = RoomTimes.objects \
        .order_by('time') \
        .values('time') \

    categories = list()
    times = list()
    occupied = list()

    for entry in data:
        categories.append('%s' % entry['room'])
        occupied.append(entry['occupied'])

    for entry in dataTime:
        times.append('%s' % entry['time'])

    # print("Room organized by time: ",categories)
    # print("Times in order: ", times)
    # print("Occupied: ", occupied)

    ##create a list of these
        ## room_name
        ## hashmap time_range [10-11,11-12,.....
    #no duplicates
    c = set(categories)
    c1 = list(c)

    occupiedRooms = defaultdict(lambda: 'nullERROR')

    for entry in c1:
        occupiedRooms[entry] = defaultdict(lambda: 0)

    for ind in range (0, len(categories)):
        t = 10
        roomName = categories[ind]
        cT = times[ind]
        currTime = datetime.datetime.strptime(cT, "%H:%M")
        occupiedNum = occupied[ind]
        for time in range (10,20):
            todayTime = datetime.datetime.now().replace(hour=time, minute=0, second=0, microsecond=0).strftime("%H:%M")
            todayT = datetime.datetime.strptime(todayTime,"%H:%M")
            if(todayT > currTime):
                break
            t = time
        timeRange = occupiedRooms[roomName]
        timeRange[t] = timeRange[t] + occupiedNum
        if occupied[ind] > 1:
            if ind + occupied[ind]-1 >= len(categories):
                break
            else:
                ind = ind + occupied[ind]-1;


    finalTimeRanges = defaultdict(lambda: list())

    for room in c1:
        roomData = occupiedRooms[room]
        for time in range (10,20):
            ftr = finalTimeRanges[time]
            ftr.append(roomData[time])

    # for entry in finalTimeRanges:
    #     print("Entry: ",entry)
    #     print("Value: ", finalTimeRanges[entry])



    chart = {
        'chart': {
            'type': 'bar'
        },
        'title': {
            'text': 'Room Occupancy Times through the Week'
        },
        'xAxis': {
            'categories': c1
        },
        'yAxis':{
            'title': {'text': 'Number of times used'},
        },
        'series': [{
        'name': '10-11am',
        'data': finalTimeRanges[10]
    }, {
        'name': '11-12pm',
        'data': finalTimeRanges[11]
    }, {
        'name': '12-1pm',
        'data': finalTimeRanges[12]
    }, {
        'name': '1-2pm',
        'data': finalTimeRanges[13]
    }, {
        'name': '2-3pm',
        'data': finalTimeRanges[14]
    }, {
        'name': '3-4pm',
        'data': finalTimeRanges[15]
    }, {
        'name': '4-5pm',
        'data': finalTimeRanges[16]
    }, {
        'name': '5-6pm',
        'data': finalTimeRanges[17]
    }, {
        'name': '6-7pm',
        'data': finalTimeRanges[18]
    },{
        'name': '7-8pm',
        'data': finalTimeRanges[19]
    }]
    }

    dump = json.dumps(chart)

    return render(request, 'senior_des/time_graphs.html', {'chart': dump})
    # return render(request, 'senior_des/time_graphs.html', {'dataset': dataset})

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

    ten = datetime.datetime.now().replace(hour=10, minute=0, second=0, microsecond=0).strftime("%H:%M")
    eight = datetime.datetime.now().replace(hour=20, minute=0, second=0, microsecond=0).strftime("%H:%M")
    tenAM = datetime.datetime.strptime(ten,"%H:%M")
    eightPM = datetime.datetime.strptime(eight,"%H:%M")
    currTime = datetime.datetime.strptime(localtimestamp, "%H:%M")
    # Only add times between 10am - 8PM in graph! and maybe website??? not sure about that one
    if(currTime >= tenAM and currTime <= eightPM):
        roomTime.save()
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
        if "empty" not in temp:
            room.isOcc = False
        else:
            room.isOcc = True
        #print(room)

    #print(type(rooms))
    args = {'rooms' : rooms}
    return render(request, 'senior_des/error.html', args)
