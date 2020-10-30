from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from django.http import HttpResponseRedirect
from . models import *
from django.db.models import Q
import requests
import smtplib

api_key = "AIzaSyAmYWHcxVhiGEK-F_-kcO0bZI0_-Tw8rPE"

def index(request):
        return render(request, "index.html")

def createClient(request):
    errors = Client.objects.clientValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        securedPass= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        oneClient = Client.objects.create(fullName=request.POST['fullName'],companyName=request.POST['companyName'],streetAddress=request.POST['streetAddress'],email=request.POST['email'],password=securedPass,zipCode=request.POST['zipCode'], state=request.POST['state'], phone=request.POST['phone'])
        request.session['clientId'] = oneClient.id
        return redirect('/clientPage')

def loginClient(request):
    errors = Client.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
    else:
        clientsWithEmail = Client.objects.filter(email = request.POST['email'])
        request.session['clientId'] = clientsWithEmail[0].id
        return redirect('/clientPage')

def clientPage(request):
    if "clientId" not in request.session:
        return redirect('/')
    else:
        client = Client.objects.get(id=request.session['clientId'])
        
        start = "fort worth"
        end = (client.state)
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"
        r = requests.get(url + "origins=" + start + "&destinations=" + end + "&key=" + api_key)
        time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
        context = {
            'time' : time,
            'client': Client.objects.get(id=request.session['clientId']),
        }
    return render(request, "client.html", context)

def destroySession(request):
    request.session.clear()
    return redirect('/')

