from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.db.models import F


# Create your views here.

def home(request):

    if request.user.is_authenticated:
        events_user_has_enrolled_in = Participants.objects.filter(username = request.user.username)

        all_events_id = []

        for i in events_user_has_enrolled_in:
            all_events_id.append(i.eventID)
        
        all_events_enrolled_by_user = []


        for i in all_events_id:
            event = Event.objects.get(eventID = i)
            all_events_enrolled_by_user.append(event)
            
        
        user_hosted_events = Event.objects.filter(host = request.user.username)


        allevents = Event.objects.all()
        
        context = {"user_events" : all_events_enrolled_by_user, "hosted_events" : user_hosted_events, "allevents" : allevents}
        print(all_events_enrolled_by_user)
        print(user_hosted_events)

        return render(request, "index.html", context=context)
    
    else:
        return render(request, "login_signup.html")


def signup(request):
    if request.method == 'POST':
        name= request.POST['name']
        u_name = request.POST['u_name']
        email = request.POST['email']
        password = request.POST['password']

        try:
            #creating user
            myuser = User.objects.create_user(u_name,email,password)
            myuser.first_name = name
            myuser.save()
            messages.success(request, "Welcome to the Community!")

            # login the created user
            sign_uped_user = authenticate(username=u_name, password=password)
            login(request, sign_uped_user)

            return redirect("home")
        
        except:
            messages.error(request, "Username already taken, please try another one")
            return redirect("home")


def login_usr(request):
    if request.method == 'POST':
        u_name = request.POST['u_name']
        password = request.POST['password']

        try:
            login_user = authenticate(username=u_name, password=password)
            login(request, login_user)

            messages.success(request, "Welcome Back! New Events are waiting for You")

            return redirect("home")
        
        except:
            messages.error(request, "No User Found, if You are new Consider Signing up :)")
            return redirect("home")


def logout_usr(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Successfully  Logged Out")
        return redirect("home")
    return HttpResponse("404 Not Found")




def create_event(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            nameofevent = request.POST["nameofevent"]
            host = request.user.username
            desc = request.POST["desc"]
            cost = request.POST["cost"]
            place = request.POST['place']

            date = request.POST["date"]
            time = request.POST["time"]

            myevent = Event(name = nameofevent, host=host, desc=desc, cost=cost, place=place, date=date, time=time)
            myevent.save()

            messages.success(request, "Your event is created successfully")

            return redirect("myevents")

        else:
            return render(request, "create_event.html")
    
    else:
        redirect("home")


def myevents(request):
    if request.user.is_authenticated:
        events_user_has_enrolled_in = Participants.objects.filter(username = request.user.username)

        all_events_id = []

        for i in events_user_has_enrolled_in:
            all_events_id.append(i.eventID)
        
        all_events_enrolled_by_user = []


        for i in all_events_id:
            event = Event.objects.get(eventID = i)
            all_events_enrolled_by_user.append(event)
            
        
        user_hosted_events = Event.objects.filter(host = request.user.username)


        context = {"user_events" : all_events_enrolled_by_user, "hosted_events" : user_hosted_events}
            
        return render(request, "myevents.html", context=context)


    else:
        redirect("home")




def pay_n_participate(request):
    if request.method == "POST":

            username = request.user.username
            eventID = request.POST['eventid']
            print(eventID)

            participant = Participants(username = username, eventID = eventID, event=Event.objects.get(eventID = eventID))
            participant.save()

            Event.objects.filter(eventID = eventID).update(number_of_participants = F("number_of_participants") + 1)

            messages.success(request, f"You have been successfully registered for the event")

            return redirect("myevents")
    
    else:
        return HttpResponse("404")





def dummypayment(request):
    if request.method == "POST":
        eventid = request.POST['eventid']
        return render(request, "payment.html", context = {"eventid" : eventid})
    else:
        HttpResponse("404")
    


def get_editevent_details(request):
    if request.method == "POST":
        eventID = request.POST.get("eventID")
        name = request.POST.get("name")
        desc = request.POST.get('desc')
        cost = request.POST.get('cost')
        date = request.POST.get('date')
        time = request.POST.get('time')
        place = request.POST.get('place')


        context = {
            'eventID' : eventID,
            'name': name,
            'desc': desc,
            'cost': cost,
            'date': date,
            'time': time,
            'place': place
        }

        return render(request, "editevent.html", context=context)
    else:
        return HttpResponse("404")
    

def fill_edit_details(request):
    if request.method == "POST":
        eventID = request.POST.get("eventID")
        name = request.POST.get("name")
        desc = request.POST.get('desc')
        cost = request.POST.get('cost')
        date = request.POST.get('date')
        time = request.POST.get('time')
        place = request.POST.get('place')



        event = Event.objects.get(eventID = eventID)
        event.name = name
        event.desc = desc
        event.cost = cost
        event.date = date
        event.time = time
        event.place = place

        event.save()

        messages.success(request, "Event Edited Successfully")
        return redirect("myevents")
    

def manage_cancellation(request):
    if request.method == "POST":
        eventID = request.POST["eventID"]
        context = {"eventID" : eventID}

        return render(request, "cancellation_refund.html", context=context)


def cancel_participation(request):
    if request.method == 'POST':
        eventID = request.POST["eventID"]
        username = request.user.username

        event = Participants.objects.filter(eventID = eventID, username = username)
        event.delete()

        Event.objects.filter(eventID = eventID).update(number_of_participants = F("number_of_participants") - 1)


        messages.success(request, "Cancellation & Refund Successful.")

        return redirect("myevents")

    else:
        return HttpResponse("404")
    





def search(request):
    if request.user.is_authenticated:
        query = request.GET["search"]
        events_user_has_enrolled_in = Participants.objects.filter(username = request.user.username)

        all_events_id = []

        for i in events_user_has_enrolled_in:
            all_events_id.append(i.eventID)
        
        all_events_enrolled_by_user = []


        for i in all_events_id:
            try:
                event = Event.objects.get(eventID = i, name__icontains = query)
                all_events_enrolled_by_user.append(event)
            
            except:
                break
            
        
        user_hosted_events = Event.objects.filter(host = request.user.username, name__icontains = query)


        allevents = Event.objects.filter(name__icontains = query)
        
        context = {"user_events" : all_events_enrolled_by_user, "hosted_events" : user_hosted_events, "allevents" : allevents}

        return render(request, "search.html", context=context)
    



def mark_as_completed(request):
    if request.user.is_authenticated:
        if request.method =="POST":
            eventID = request.POST["eventID"]

            event = Event.objects.get(eventID = eventID)
            event.completed = 1
            event.save()

            messages.success(request, "Event Marked Completed!")

            return redirect("myevents")
        
        else:
            return HttpResponse(404)
        
    else:
        return HttpResponse("404")




def participants(request):
    if request.method == "POST":
        eventID = request.POST["eventID"]

        all_participants = Participants.objects.filter(eventID = eventID)

        context={"participants" : all_participants, "eventname" : Event.objects.get(eventID = eventID).name}

        return render(request, "participants.html", context=context)
    
    else:
        return HttpResponse("404")
    


def q_and_a(request):
    if request.user.is_authenticated:

        if request.method == "POST":

            eventID = request.POST["eventID"]
            username = request.user.username
            desc = request.POST["desc"]

            MyQuestion = Comments(eventID = eventID, username = username, desc = desc)
            MyQuestion.save()

            messages.success(request, "Your Question is posted successfully!")


        eventID = request.GET["eventID"]

        event = Event.objects.get(eventID = eventID)

        comments = Comments.objects.filter(eventID = eventID)

        context = {"event" : event, "comments" : comments}

        return render(request, "QnA.html", context = context)
    

    

    else:
        return HttpResponse("404")
    



