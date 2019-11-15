from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Users,Trips
import bcrypt

def logregpage(request):
    if 'userid' in request.session:
        return redirect('/dashboard')
    return render(request, 'examapp/logreg.html')

def process(request):
    if 'userid' in request.session:
        return redirect('/dashboard')
    if request.POST['which_form']== 'register':
        errors = Users.objects.basic_validator(request.POST)
        if len(errors)> 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            first=request.POST['fname']     
            last=request.POST['lname']
            email=request.POST['email']          
            user1=Users.objects.filter(email=email)
            password=request.POST['pw']
            hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            Users.objects.create(first=first, last=last, email=email,password=hash1)
            request.session['email']=email
            curuser=Users.objects.last()
            request.session['userid'] = curuser.id
        return redirect('/dashboard')
    
    if request.POST['which_form']=='login':
        errors = Users.objects.login_validator(request.POST)
        if len(errors)> 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        email=request.POST['email']
        user1=Users.objects.filter(email=email)
        curuser=user1[0]
        if bcrypt.checkpw(request.POST['pw'].encode(), curuser.password.encode()):
            request.session['userid'] = curuser.id
            return redirect('/dashboard')
        else:
            return redirect('/')


        return redirect('/dashoard')

def dashboard(request):
    if 'userid' not in request.session:
        return redirect('/')
    curuser=Users.objects.get(id=request.session['userid'])
    context={
        'curuser':Users.objects.get(id=request.session['userid']),
        'usertrips':curuser.trips.all()
    }
    return render(request, 'examapp/dashboard.html', context)
def newtrip(request):
    if 'userid' not in request.session:
        return redirect('/')
    context={
        'curuser':Users.objects.get(id=request.session['userid'])
    }
    return render(request, 'examapp/newtrip.html' ,  context)
def destroy(request):
    if 'userid' not in request.session:
        return redirect('/')
    request.session.clear()
    return redirect('/')

def createtrip(request):
    if 'userid' not in request.session:
        return redirect('/')
    errors = Trips.objects.trip_validator(request.POST)
    if len(errors)> 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')
    destination=request.POST['destination']
    start=request.POST['start']
    end=request.POST['end']
    plan=request.POST['plan']
    userlink=Users.objects.get(id=request.session['userid'])
    Trips.objects.create(destination=destination, start=start,end=end,plan=plan,userlink=userlink)
    return redirect('/')

def deltetrip(request,idnum):
    if 'userid' not in request.session:
        return redirect('/')
    Trips.objects.get(id=idnum).delete()
    return redirect('/dashboard')
def editrip(request,idnum):
    if 'userid' not in request.session:
        return redirect('/')
    trip=Trips.objects.get(id=idnum)
  
    context={
        'curuser':Users.objects.get(id=request.session['userid']),
        'trip':trip,
    }

    return render(request, 'examapp/tripedit.html',context)
def edit(request, idnum):
    if 'userid' not in request.session:
        return redirect('/')
    trip=Trips.objects.get(id=idnum)
    errors = Trips.objects.trip_validator(request.POST)
    if len(errors)> 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/trips/edit/{trip.id}')
    

    
    trip.plan=request.POST['plan']
    trip.start=request.POST['start']
    trip.end=request.POST['end']
    trip.destination=request.POST['destination']
    trip.save()
    return redirect('/dashboard')

def tripinfo(request,idnum):
    if 'userid' not in request.session:
       return redirect('/')
    context={
        'trip':Trips.objects.get(id=idnum),
        'curuser':Users.objects.get(id=request.session['userid'])
    }
    return render(request, 'examapp/tripinfo.html',context)
    

    

