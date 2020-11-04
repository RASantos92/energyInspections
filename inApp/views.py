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
        oneClient = Client.objects.create(fullName=request.POST['fullName'],companyName=request.POST['companyName'],streetAddress=request.POST['streetAddress'],email=request.POST['email'],password=securedPass,zipCode=request.POST['zipCode'], city=request.POST['city'], phone=request.POST['phone'])
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
        end = (client.city)
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"
        r = requests.get(url + "origins=" + start + "&destinations=" + end + "&key=" + api_key)
        time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
        clientTime = giveExtraTime(time)
        context = {
            'time' : clientTime,
            'client': Client.objects.get(id=request.session['clientId']),
        }
    return render(request, "client.html", context)

def destroySession(request):
    request.session.clear()
    return redirect('/')


def giveExtraTime(time):
    newStr = ""
    output = ""
    if len(time) == 7:
        hours = 0
        newStr += time[0]
        newStr += time[1]
        for i in range(2,len(time),1):
            output += time[i]
        x = int(newStr) + 60
        finalOutput = str(x) + output
        if x > 60:
            while x > 60:
                x += -60
                hours += 1 
            if hours == 1:
                print(hours)
                x = (str(hours) + " hour " + str(x))
            if hours > 1:
                print(hours)
                x = (str(hours) + " hours " + str(x))
            finalOutput = x + output
        return finalOutput
    if len(time) == 14:
        newStr += time[0]
        for i in range(1,len(time),1):
            output += time[i]
        x = int(newStr) + 1
        finalOutput = str(x) + output
        print(str(x) + output)
        return finalOutput
