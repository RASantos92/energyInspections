from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from django.http import HttpResponseRedirect
from . models import *
from django.db.models import Q



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
        return redirect('/')

def loginClient(request):
    valErrors = Client.objects.loginValidator(request.POST)
    if len(valErrors) > 0:
        for value in valErrors.values():
            messages.loginErrors(request, value)
        return redirect('/')
    else:
        clientWithEmail = Client.objects.filter(email = request.POST['email'])
        request.session['userId'] = usersWithEmail[0].id
        return redirect('/')