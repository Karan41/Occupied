from django.shortcuts import render, HttpResponse

from senior_des.models import Rooms

# Create your views here.

def room(request):
    rooms = Rooms.objects.all()
    for room in rooms:
        #print(room);
        room.text = room
        temp = room.room_arr()
        #print(type(temp))
        #print(temp)
        #print(rooms)
    print(type(rooms))
    args = {'rooms' : rooms }
    return render(request, 'senior_des/room.html', args) 
    
def home(request):
    return render(request, 'senior_des/homepage/startbootstrap-agency-master/index.html')

def database(request):
    #add to database the request sent
    print('WHATS GOING ON:  ', request)
    s = request.META['QUERY_STRING']


    print(s)
    each_info = s.split('+')
    error_message = {}
    if (each_info[0] != 'b9c4t5tac1') :
       error_message = 'BAD USER (in future should lock this user out of website for 5 min)'
       args = {'message' : error_message}
       return render(request, 'senior_des/error.html', args)
    elif (len(each_info) != 4):
        print("how many splits: ", each_info)
        error_message ['message'] = 'not enough input parameters. Should be ?Password+room_name+room_number+is_occupied'
        args = {'message' : error_message}
        return render(request, 'senior_des/error.html', args)

    if (each_info[3] == 'false'):
        each_info[3] = False
    elif (each_info[3] == 'true'):
        each_info[3] = True
    else:
        error_message ['message'] = 'is_occupied is not the right value: enter false or true for it'
        args = {'message' : error_message}
        return render(request, 'senior_des/error.html', args)



    x = Rooms (room_name=each_info[1], room_number=each_info[2], is_occupied=bool(each_info[3]))
    r = Rooms.objects.all().filter(room_name=each_info[1]).filter(room_number=each_info[2])
        
    print (type(Rooms.objects.all()))
    if(len(r) == 0):
        x.save()
        print("Room doesn't exist")
        #if room does exist then update the state
    else:
        o = r.first()   
        print("here is the room being updated: ", o)
        o.is_occupied = x.is_occupied
        o.save() 
    error_message = 'successful room change: updated room ', each_info[1], ' with room number of ',each_info[2]
    print (error_message , ' TESTINGGGGG')
    args = {'message' : error_message}
    return render(request, 'senior_des/error.html', args)


