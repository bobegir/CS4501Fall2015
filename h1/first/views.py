from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password

from first import models
from django.core import serializers
from datetime import datetime, timedelta

import os
import base64

import json

def model_to_json(model):
	data = serializers.serialize('json',[model,])
	struct = json.loads(data)
	data = json.dumps(struct[0])
	return data

def index(request):
    return HttpResponse("Hello World!")

def add_vehicle(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be POST'})
    new_car = models.Vehicle()
    if 'max_seats' in request.POST:
        new_car.max_seats = request.POST['max_seats']
    if 'trunk_space' in request.POST:
        new_car.trunk_space = request.POST['trunk_space']
    if 'notes' in request.POST:
        new_car.notes = request.POST['notes']
    if 'make' in request.POST:
        new_car.make = request.POST['make']
    if 'model' in request.POST:
        new_car.model = request.POST['model']
    if 'year' in request.POST:
        new_car.year = request.POST['year']
    if 'color' in request.POST:
        new_car.color = request.POST['color']
    if 'plates' in request.POST:
        new_car.plates = request.POST['plates']
    if 'uninsured' in request.POST:
        new_car.uninsured = request.POST['uninsured']
    if 'road_assistance' in request.POST:
        new_car.road_assistance = request.POST['road_assistance']
    if 'accomodations' in request.POST:
        new_car.accomodations = request.POST['accomodations']
    new_car.save()
    user = models.User.objects.get(username=request.POST['username'])
    user.vehicle = models.Vehicle.objects.latest('pk')
    user.save()
    return JsonResponse({'ok':True, 'log': 'Added vehicle'})

def car_list(request):
    cars = models.Vehicle.objects.all()
    formatted = [str(c.id) + str(c.make) + str(c.model) + '\n' for c in cars]
    return JsonResponse(serializers.serialize("json", models.Vehicle.objects.all()),safe=False)

def get_car(request, car):
    if request.method != 'GET':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be get'})
    try:
        v = models.Vehicle.objects.get(pk=car)
    except models.Vehicle.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Failed to find car id ' + car})
    ret_val = model_to_json(v)
    return JsonResponse({'ok':True,'car':ret_val})

def update_car(request, car):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be POST'})
    try:
        this_car = models.Vehicle.objects.get(pk=car)
    except:
        return JsonResponse({'ok': False, 'error': 'Failed to find car id ' + car})
    if 'max_seats' in request.POST:
        this_car.max_seats = request.POST['max_seats']
    if 'trunk_space' in request.POST:
        this_car.trunk_space = request.POST['trunk_space']
    if 'notes' in request.POST:
        this_car.notes = request.POST['notes']
    if 'make' in request.POST:
        this_car.make = request.POST['make']
    if 'model' in request.POST:
        this_car.model = request.POST['model']
    if 'year' in request.POST:
        this_car.year = request.POST['year']
    if 'color' in request.POST:
        this_car.color = request.POST['color']
    if 'plates' in request.POST:
        this_car.plates = request.POST['plates']
    if 'uninsured' in request.POST:
        this_car.uninsured = request.POST['uninsured']
    if 'road_assistance' in request.POST:
        this_car.road_assistance = request.POST['road_assistance']
    if 'accomodations' in request.POST:
        this_car.accomodations = request.POST['accomodations']
    this_car.save()
    return JsonResponse({'ok':True, 'log': 'Updated vehicle ' + car})

def add_user(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be post'})
    #first, last, email, password, address, phone, payment type, gender, license number, age, active
    new_user = models.User()
    if 'username' in request.POST:
        new_user.username = request.POST['username']
    if 'first' in request.POST:
        new_user.first = request.POST['first']
    if 'last' in request.POST:
        new_user.last = request.POST['last']
    if 'email' in request.POST:
        new_user.email = request.POST['email']
    if 'password' in request.POST:
        new_user.password = make_password(request.POST['password'])
    if 'city' in request.POST:
        new_user.city = request.POST['city']
    if 'state' in request.POST:
        new_user.state = request.POST['state']
    if 'phone' in request.POST:
        new_user.phone_number = request.POST['phone']
    if 'payment_type' in request.POST:
        new_user.payment_type = request.POST['payment_type']
    if 'gender' in request.POST:
        new_user.gender = request.POST['gender']
    if 'age' in request.POST:
        new_user.age = request.POST['age']
    new_user.save()
    return JsonResponse({'ok':True, 'log': 'User Created'})

def update_user(request, user):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be POST'})
    try:
        this_user = models.User.objects.get(pk=user)
    except:
        return JsonResponse({'ok': False, 'error': 'Failed to find user id ' + user})
    if 'first' in request.POST:
        this_user.first = request.POST['first']
    if 'last' in request.POST:
        this_user.last = request.POST['last']
    if 'email' in request.POST:
        this_user.email = request.POST['email']
    if 'city' in request.POST:
        this_user.city = request.POST['city']
    if 'state' in request.POST:
        this_user.state = request.POST['state']
    if 'phone' in request.POST:
        this_user.phone = request.POST['phone']
    if 'payment_type' in request.POST:
        this_user.payment = request.POST['payment_type']
    if 'gender' in request.POST:
        this_user.gender = request.POST['gender']
    if 'age' in request.POST:
        this_user.age = request.POST['age']
    this_user.save()
    return JsonResponse({'ok':True, 'log': 'User Info Editted'})

def update_password(request, user):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be POST'})
    try:
        recover_user = models.User.objects.get(pk=user)
    except:
        return JsonResponse({'ok': False, 'error': 'Failed to find user id ' + user})
    if 'password' in request.POST:
        recover_user.password = make_password(request.POST['password'])
    return JsonResponse({'ok':True, 'log': 'Password Changed'})

def get_user(request, user):
    if request.method != 'GET':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be GET'})
    try:
        this_user = models.User.objects.get(pk=user)
    except:
        return JsonResponse({'ok': False, 'error': 'Failed to find user id ' + user})
    ret_val = model_to_json(this_user)
    return JsonResponse({'ok': True,'user': ret_val})

def get_user_by_name(request):
    if request.method != 'GET':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be GET'})
    user = request.GET['user']
    try:
        this_user = models.User.objects.get(username=user)
    except:
        return JsonResponse({'ok': False, 'error': 'Failed to find user ' + user})
    ret_val = model_to_json(this_user)
    return JsonResponse({'ok': True,'user': ret_val})
        
def deactivate_user(request, user):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be POST'})
    if 'deactivate' in request.POST:
        try:
            deactivate_user = models.User.objects.get(pk=user)
        except:
            return JsonResponse({'ok': False, 'error': 'Failed to find user id' + user})
        deactivate_user.active = False
        deactivate_user.save()
    return JsonResponse({'ok':True, 'log': 'User Account Deactivated'})

def get_auth(request): 
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be POST'})
    username = request.POST['username']
    password = request.POST['password']
    try:
        this_user = models.User.objects.get(username=username)
        hashed_pass = this_user.password
    except:
        return JsonResponse({'ok': False, 'error': 'User account was not found'})
    check = check_password(password,hashed_pass)
    if check:
        models.AuthTable.objects.filter(user_id=this_user).delete()
        new_auth = models.AuthTable()
        new_auth.user_id = this_user
        new_auth.date_created = datetime.now()
        new_auth.authenticator = base64.b64encode(os.urandom(32)).decode('utf-8')
        new_auth.save()
        return JsonResponse({'ok': True, 'log': 'Login successful', 'auth': new_auth.authenticator})
    else:
        return JsonResponse({'ok': False, 'error': 'Password was incorrect'})

def check_auth(auth):
    try:
        this_auth = models.AuthTable.objects.get(authenticator=auth)
    except:
        return False
    #Should we return the user and stuff too? Or just let that one be?
    return True

def is_auth(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be POST'})
    auth = request.POST['auth']
    time_limit = datetime.now() - timedelta(hours=6)
    models.AuthTable.objects.filter(date_created__lt=time_limit).delete()
    if check_auth(auth):
        auth_obj = models.AuthTable.objects.get(authenticator=auth)
        return JsonResponse({'ok': True, 'username': auth_obj.user_id.username})
    else:
        return JsonResponse({'ok': False, 'error': 'Invalid authenticator'})

def revoke_auth(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be POST'})
    auth = request.POST['auth']
    try:
        this_auth = models.AuthTable.objects.get(authenticator=auth)
    except:
        return JsonResponse({'ok': True, 'log': 'Auth not found'})
    this_auth.delete()
    time_limit = datetime.now() - timedelta(hours=6)
    models.AuthTable.objects.filter(date_created__lt=time_limit).delete()
    return JsonResponse({'ok': True, 'log': 'Auth removed'})

def create_ride(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be POST'})
    new_ride = models.Ride()    
    if 'leave_time' in request.POST:
        new_ride.leave_time = datetime.strptime(request.POST['leave_time'], '%H:%M')
    if 'arrive_time' in request.POST:
        new_ride.arrive_time = datetime.strptime(request.POST['arrive_time'], '%H:%M')
    if 'destination' in request.POST:
        new_ride.destination = request.POST['destination']
    if 'start' in request.POST:
        new_ride.start = request.POST['start']
    if 'comments' in request.POST:
        new_ride.comments = request.POST['comments']
    if 'max_miles_offroute' in request.POST:
        new_ride.max_miles_offroute = request.POST['max_miles_offroute']
    user = models.User.objects.get(username=request.POST['username'])
    vehicle = user.vehicle
    new_ride.driver = user
    new_ride.car = vehicle
    new_ride.save()
    return JsonResponse({'ok':True, 'log': 'Ride Created', 'id': new_ride.pk})
        
def ride_list(request):
    rides = models.Ride.objects.all()
    formatted = [model_to_json(ride) for ride in rides]
    return JsonResponse({'ok': True, 'ride': formatted})

def active_ride_list(request):
    rides = models.Ride.objects.filter(active=True)
    formatted = [model_to_json(ride) for ride in rides]
    return JsonResponse({'ok': True, 'ride': formatted})
    
def update_ride(request, ride):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be POST'})
    try:
        this_ride = models.Ride.objects.get(pk=ride)
    except:
        return JsonResponse({'ok': False, 'error': 'Failed to find ride id: ' + ride})
    if 'leave_time' in request.POST:
        this_ride.leave_time = request.POST['leave_time']
    if 'arrive_time' in request.POST:
        this_ride.arrive_time = request.POST['arrive_time']
    if 'destination' in request.POST:
        this_ride.destination = request.POST['destination']
    if 'start' in request.POST:
        this_ride.start = request.POST['start']
    if 'comments' in request.POST:
        this_ride.comments = request.POST['comments']
    if 'max_miles_offroute' in request.POST:
        this_ride.max_miles_offroute = request.POST['max_miles_offroute']
    this_car.save()
    return JsonResponse({'ok':True, 'log': 'Ride updated'})
    
def get_ride(request, ride):
    if request.method != 'GET':
        return JsonResponse({'ok': False, 'error': 'Wrong request type, should be get'})
    try:
        ride = models.Ride.objects.get(pk=ride)
    except models.Ride.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Failed to find ride id: ' + ride})
    ret_val = serializers.serialize('json',[ride,])
    return JsonResponse({'ok':True,'car':ret_val})
    
def deactivate_ride(request, ride):
    if request.method != 'POST':
            return JsonResponse({'ok': False, 'error': 'Wrong request type, should be POST'})
    if 'deactivate' in request.POST:
        try:
            deactivate_ride = models.User.objects.get(pk=ride)
        except:
            return JsonResponse({'ok': False, 'error': 'Failed to find ride id' + user})
        deactivate_ride.active = False
        deactivate_ride.save()
    return JsonResponse({'ok':True, 'log': 'Ride Deactivated'})
