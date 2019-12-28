# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#import webcam.admin # needed to show the right widget in the admin
from django.db import models
#from bbio.libraries.WebCam import WebCam

#from webcam.fields import CameraField
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    #return HttpResponse('''<h1>home</h1> ''')
    
    return render(request, 'index.html')