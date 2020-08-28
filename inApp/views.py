from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from django.http import HttpResponseRedirect
from . models import *



def index(request):
    return render(request, "index.html")