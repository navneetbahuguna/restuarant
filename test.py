from __future__ import unicode_literals
import numpy as np
from django.shortcuts import render
from django.template import loader
import subprocess
"""from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework import views, status
from rest_framework.decorators import api_view
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.template import RequestContext
from StringIO import StringIO
from zipfile import ZipFile
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, Http404, HttpResponsePermanentRedirect
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo import mongo_client
from django.views.generic import TemplateView
from uuid import uuid4
import urllib, datetime"""
# Create your views here.
from django.http import HttpResponse
#from django.core.context_processors import csrf
import mongoengine
from pymongo import MongoClient
import numpy as np
import cv2, os
import sqlite3
import PIL 
import pickle
from PIL import Image
faceDetect = cv2.CascadeClassifier('/media/navneet/72f83045-b7eb-4237-a111-1f6156ea4496/django/pro1/polls/haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)
try:
    rec = cv2.face.LBPHFaceRecognizer_create()
except Exception as e:
    print(e)
rec.read('trainingData.yml')

font = cv2.FONT_HERSHEY_SIMPLEX

def getProfile(id):
    client = MongoClient('mongodb://localhost:27017/')
    # Accessing a Database
    mydb = client.user_db
    #conn = sqlite3.connect("FaceBase.db")
    data = mydb.signup.find_one({"ID":str(id)})
    #print('detail', data['ID'])
    #profile = None
    """for row in cursor:
        profile = row
    conn.close()"""
    return data
        

while (True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 2)
        id_, conf = rec.predict(gray[y:y+h, x:x+w])
        print('id_',id_,conf)
        #profile = getProfile(id)
        data = getProfile(id_)
        print(data)
        name = data['FullName']
        user_id = data['user_name']

        if( data != None):
            cv2.putText(img, str(name), (x, y+h+30), font, 1.0, 255, 2)
            
            cv2.putText(img, str(user_id), (x, y+h+60), font, 1.0, 255, 2)
            
            #cv2.putText(img, str(profile[2]), (x, y+h+90), font, 1.0, 255, 2)
            
            #cv2.putText(img, str(profile[3]), (x, y+h+120), font, 1.0, 255, 2)

            
        
    cv2.imshow("face", img)

    if cv2.waitKey(33) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
