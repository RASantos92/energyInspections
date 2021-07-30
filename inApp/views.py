from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from django.http import HttpResponseRedirect
from . models import *
from django.db.models import Q
from datetime import datetime
import requests
import smtplib

api_key = "AIzaSyAmYWHcxVhiGEK-F_-kcO0bZI0_-Tw8rPE"

def index(request):
    context = {
        "pageInfo" : Admin.objects.get(id = 1)
    }
    if "clientId"  in request.session:
        return redirect('/clientPage')
    return render(request, "index.html", context)

def createClient(request):
    errors = Client.objects.clientValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        securedPass= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        oneClient = Client.objects.create(fullName=request.POST['fullName'],companyName=request.POST['companyName'],

        streetAddress=request.POST['streetAddress'],email=request.POST['email'],password=securedPass,zipCode=request.POST['zipCode'], city=request.POST['city'], phone=request.POST['phone'])
        request.session['clientId'] = oneClient.id
        oneClient.pto = 144
        return redirect('/workRequestForm')

def loginClient(request):
    errors = Client.objects.loginValidator(request.POST)
    if request.POST["email"] == "tim1969s":
        return redirect('/adminLoginPage1234561231548462858')
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
        thisclients = Client.objects.get(id=request.session['clientId'])
        reviewed = []
        notReviewed = []
        for i in thisclients.workRequests.all():
            if i.reviewed == False:
                notReviewed.append(i)
            else:
                reviewed.append(i)
        print(len(notReviewed), "test ================")
        # client = Client.objects.get(id=request.session['clientId'])
        # start = "fort worth"
        # end = (client.city)
        # url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"
        # r = requests.get(url + "origins=" + start + "&destinations=" + end + "&key=" + api_key)
        # time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
        # clientTime = giveExtraTime(time)
        context = {

            'client': Client.objects.get(id=request.session['clientId']),
            'reviewed': reviewed, 
            'notReviewed' : notReviewed
        }
    return render(request, "client.html", context)

def clientEdit(request, clientId):
    if "clientId" not in request.session:
        return redirect('/')
    if request.session["clientId"] != clientId:
        return redirect('/')
    context = {
        'client' : Client.objects.get(id = clientId)
    }
    return render(request,"clientEdit.html",context)

def clientEditProcess(request):
    client = Client.objects.get(id = request.session["clientId"])
    if request.POST["companyName"] != "":
        client.missionS = request.POST["companyName"]
    if request.POST["fullName"] != "":
        client.fullName = request.POST["fullName"]
    if request.POST["zipCode"] != "":
        client.zipCode = request.POST["zipCode"]
    if request.POST["email"] != "":
        client.email = request.POST["email"]
    if request.POST["streetAddress"] != "":
        client.streetAddress = request.POST["streetAddress"]
    if request.POST["city"] != "":
        client.city = request.POST["city"]
    if request.POST["phone"] != "":
        client.phone = request.POST["phone"]
    client.save()
    return redirect('/clientPage')


def aboutWhy(request):
    if 'clientId' in request.session:
        context = {
            'client': Client.objects.get(id=request.session['clientId']),
        }
        return render(request, "why.html",context)
    return render(request,"why.html")

def services(request):
    if 'clientId' in request.session:
        thisclients = Client.objects.get(id=request.session['clientId'])
        reviewed = []
        notReviewed = []
        for i in thisclients.workRequests.all():
            if i.reviewed == False:
                notReviewed.append(i)
            else:
                reviewed.append(i)
        context = {
            "reviewed" : reviewed,
            'client': Client.objects.get(id=request.session['clientId']),
            'notReviewed' : notReviewed
        }
        return render(request, "services.html",context)
    return render(request,"services.html")

def destroySession(request):
    request.session.clear()
    return redirect('/')

def workRequestForm(request):
    if 'clientId' in request.session:
        context = {
                # 'time' : clientTime,
                'client': Client.objects.get(id=request.session['clientId']),
            }
        return render(request, "workRequest.html",context)
    messages.error(request, "You can to register or login to fill out a inspection request, or you can call at <placeholder> or email at<placeholder@gmail.com>")
    return redirect('/clientPage')

def workRequestProcess(request):
    errors = WorkRequest.objects.workRequestValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/workRequestForm')
    else:
        print(request.POST["prefferedInspectionDate"] == "")
        if request.POST["prefferedInspectionDate"] == "":
            newWorkRequest = WorkRequest.objects.create(client = Client.objects.get(id=request.session['clientId']),jobLocation = request.POST["jobLocation"], phone = request.POST["phone"],prefferedInspectionDate = datetime.now() , comment = request.POST["comment"])
        else:
            newWorkRequest = WorkRequest.objects.create(client = Client.objects.get(id=request.session['clientId']),jobLocation = request.POST["jobLocation"], phone = request.POST["phone"],prefferedInspectionDate = request.POST["prefferedInspectionDate"], comment = request.POST["comment"])
        print(newWorkRequest)
        return redirect('/clientPage')
def deleteWorkR(request, wRId):
    wR = WorkRequest.objects.get(id = wRId)
    wR.delete()
    return redirect('/clientPage')
# ===========================================================================================
# ==================================Admin====================================================
# ===========================================================================================
def adminPage(request):
    if "adminId" not in request.session:
        return redirect('/')
    context = {
        'workRequest': WorkRequest.objects.all()
    }
    return render(request,"admin.html",context)

def adminShow(request,clientId):
    if "adminId" not in request.session:
        return redirect('/')
    context = {
        # 'time' : clientTime,
        'client': Client.objects.get(id=clientId),
    }
    return render(request,"adminShow.html",context)

def reviewed(request,requestId):
    wRequest = WorkRequest.objects.get(id=requestId)
    wRequest.reviewed = True
    wRequest.save()
    return redirect('/adminPage')

def adminLoginPage(request):
    return render(request,"adminLogin.html")

def adminLogin(request):
    errors = Admin.objects.adminValidator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
    else:
        admin = Admin.objects.filter(fullName = request.POST['fullName'])
        request.session['adminId'] = admin[0].id
    return redirect('/adminPage')

def adminRegister(request):
    if(request.POST["adminCode"] != "garyReinCold69"):
        return redirect("/")
    securedPass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newAdmin = Admin.objects.create(fullName=request.POST['fullName'],password = securedPass)
    request.session['adminId'] = newAdmin.id
    return redirect('/adminPage')

def adminEdit(request):
    if "adminId" not in request.session:
        return redirect('/')
    admin = Admin.objects.get(id = request.session["adminId"] )
    context = {
        "admin" : Admin.objects.get(id = request.session["adminId"] )
    }
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++",admin.fullName, admin.missionS)
    return render(request,"adminEdit.html", context)

def adminEditProcess(request):
    admin = Admin.objects.get(id = request.session["adminId"])
    if request.POST["missionS"] != "":
        admin.missionS = request.POST["missionS"]
    if request.POST["whyLife"] != "":
        admin.whyLife = request.POST["whyLife"]
    if request.POST["OurGuarantee"] != "":
        admin.OurGuarantee = request.POST["OurGuarantee"]
    if request.POST["tailorFit"] != "":
        admin.tailorFit = request.POST["tailorFit"]
    admin.save()
    return redirect("/")

def inspectionRequestView(request,wRId):
    context ={
        "workR" : WorkRequest.objects.get(id = wRId)
    }
    return render(request, "showWorkR.html", context)

def root(request):
    return redirect("/blogs")


# def giveExtraTime(time):
#     newStr = ""
#     output = ""
#     if len(time) == 7:
#         hours = 0
#         newStr += time[0]
#         newStr += time[1]
#         for i in range(2,len(time),1):
#             output += time[i]
#         x = int(newStr) + 60
#         finalOutput = str(x) + output
#         if x > 60:
#             while x > 60:
#                 x += -60
#                 hours += 1 
#             if hours == 1:
#                 print(hours)
#                 x = (str(hours) + " hour " + str(x))
#             if hours > 1:
#                 print(hours)
#                 x = (str(hours) + " hours " + str(x))
#             finalOutput = x + output
#         return finalOutput
#     if len(time) == 14:
#         newStr += time[0]
#         for i in range(1,len(time),1):
#             output += time[i]
#         x = int(newStr) + 1
#         finalOutput = str(x) + output
#         print(str(x) + output)
#         return finalOutput
        


# testDate="12/01/1992"
# testDate1="12/01/1992"
# print(testDate <= testDate1)

