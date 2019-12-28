# install cv2 latest 
# pip install opencv-python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import numpy as np
from scipy import stats
#import statistics

from django.shortcuts import render
from django.template import loader
import subprocess
from rest_framework.exceptions import ParseError
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
import urllib, datetime
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
from uuid import uuid4


def capture_Image(idd):
    
    sampleNumber = 0
    try:
        faceDetect = cv2.CascadeClassifier("/media/navneet/72f83045-b7eb-4237-a111-1f6156ea4496/django/pro1/polls/haarcascade_frontalface_default.xml")
    except Exception as e:
        print(e)
    print(faceDetect.empty(), faceDetect)
    cam = cv2.VideoCapture(0)
    while (True):
        #return render(request, 'ai.html',)
        print('1')
        print(idd)
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print('3')
        faces = faceDetect.detectMultiScale(gray, 1.3, 5, flags=cv2.CASCADE_SCALE_IMAGE)
        print('2')
        print(faces)
        for (x, y, w, h) in faces:

            print('a')
            sampleNumber = sampleNumber+1
            print('b')
            cv2.imwrite("ImageColl/"+str(idd)+'-'+str(sampleNumber)+".jpg",gray[y:y+h, x:x+w])
            print('c')
            try:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 2)
                cv2.waitKey(100)
            except Exception as e:
                print('e2',e)

        cv2.imshow("face", img)
        cv2.waitKey(1)
        if (sampleNumber>30):
            break
    cam.release()
    cv2.destroyAllWindows()

def train():
    try:
        #recognizer = cv2.createLBPHFaceRecognizer()
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        #createLBPHFaceRecognizer()
        #recognizer = cv2.face_LBPHFaceRecognizer()
    except Exception as e:
        print(e)
        pass
    path = 'ImageColl'
    print('nav')

    def getImageWithId(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

        faces = []
        Ids = []
        for imagepath in imagePaths:
            faceImg = Image.open(imagepath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            #print('faceNp',faceNp)
            ID = int((os.path.split(imagepath)[-1].split('.')[0]).split('-')[0])

            faces.append(faceNp)
            #print (ID[0])
            Ids.append(ID)
            cv2.imshow("training", faceNp)
            cv2.waitKey(10)
        return Ids, faces
    Ids, faces = getImageWithId(path)
    #print(Ids, faces)
    print('333')
    try:
        recognizer.train(faces, np.array(Ids))
        print('111')
    except Exception as e:
        print(e)
    try:
        recognizer.save('trainingData.yml')
        print('222')
    except Exception as e:
        print(e)
    cv2.destroyAllWindows()
def getProfile(id):
    client = MongoClient('mongodb://localhost:27017/')
    # Accessing a Database
    mydb = client.user_db
    #conn = sqlite3.connect("FaceBase.db")
    data = mydb.signup.find_one({"ID":str(id)})
    
    return data
def testimage():
    faceDetect = cv2.CascadeClassifier('/media/navneet/72f83045-b7eb-4237-a111-1f6156ea4496/django/pro1/polls/haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    try:
        rec = cv2.face.LBPHFaceRecognizer_create()
    except Exception as e:
        print(e)
    rec.read('trainingData.yml')

    font = cv2.FONT_HERSHEY_SIMPLEX

    
            
    total_id = []
    for i in range(20):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 2)
            id_, conf = rec.predict(gray[y:y+h, x:x+w])
            print('id_',id_,conf)
            total_id.append(int(id_))
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
    print('total_id',total_id)
    Fmode = max(set(total_id), key=total_id.count)
    print('fmode',Fmode)
    cam.release()
    cv2.destroyAllWindows()
    return Fmode
    


def index(request):
    if request.GET.get("signup_with_Image"):
        
        print('Login button')
        Signid_ = request.GET.get('Signupid','default').encode('utf-8')
        Signpassword = request.GET.get('Signuppass','default')
        if(len(Signid_)> 1 and len(Signpassword)>1 and 'default' not in Signpassword and 'default' not in Signid_):
            
            FullName = request.GET.get('Full_Name','default')
            dob = request.GET.get('dob','default')
            phone = request.GET.get('phone','default')
            print(dob)
            client = MongoClient('mongodb://localhost:27017/')
            # Accessing a Database
            mydb = client.user_db
            #mydb = client['test_database_1']
            print('database',mydb)
            if int(mydb.signup.count()) < 1:
                IDD = 1
                print('Idd',  IDD)
            else:
                IDD = mydb.signup.find()
                IDD = max([int(doc['ID']) for doc in IDD])
                print('old data',IDD)
                IDD = IDD + 1
                print('new IDD', IDD)
            print('IID', IDD)
            Cap_data = capture_Image(IDD)
            train_data = train()
            record_id = mydb.signup.insert({"user_name":str(Signid_),
                                            "password":str(Signpassword),
                                            "FullName":str(FullName),
                                            "dob":str(dob),
                                            "phone":str(phone),
                                            "ID":str(IDD)
                                            })
        print('1')
        return HttpResponseRedirect( 'registration.html',)
            


    elif request.GET.get("login_with_Email"):
        print('login_with_Image')
        id_ = request.GET.get('id','default')
        password = request.GET.get('pass','default')
        if(len(id_)> 1 and len(password)>1 and 'default' not in password and 'default' not in id_):

            #print(id_,password)
            client = MongoClient('mongodb://localhost:27017/')
            # Accessing a Database
            mydb = client.user_dbcls
            for data in mydb.signup.find({"user_name": str(id_)}):
                #print('data',data,data['password'].encode('utf-8'))
                if (str(password) == data['password'].encode('utf-8') ):
                    return render(request, 'home.html',)
                else:
                    return render(request, 'registration.html',)

    #else:
    #    pass
    elif request.GET.get("login_with_Image"):
        client = MongoClient('mongodb://localhost:27017/')
        # Accessing a Database
        mydb = client.user_db
        #mydb = client['test_database_1']
        print('database',mydb)
        if int(mydb.signup.count()) < 1:
            return render(request, 'registration.html',)
        else:
            print('login page')
            test_data = testimage()
            data = getProfile(test_data)
            print('data',data)
            name = data['FullName']
            user_id = data['user_name']
            request.POST.get("name", "")

            return render(request, 'home.html',{
                            'name':name,
                            'email_id':user_id
                        })
    
    else:
        return render(request, 'registration.html',)
    Cap_data = None
    #reload(index)
    print('******')
    return HttpResponseRedirect(request, 'registration.html',)

    
    
    

def about(request):

    #print('request')
    return render(request, 'about.html',)
    #return HttpResponse('''<h1>about</h1> ''')


    
def contact(request):
    #return HttpResponse('''<h1>contact</h1> ''')
    return render(request, 'contact.html',)

def branch(request):
    #return HttpResponse('''<h1>branch</h1> ''')
    return render(request, 'branch.html',)

def form(request):
    #return HttpResponse('''<h1>form</h1> ''')
    return render(request, 'registration.html',)

def home(request):
    #return HttpResponse('''<h1>form</h1> ''')
    return render(request, 'home.html',)



def insertOrUpdate(Id, Name):
    conn = sqlite3.connect("FaceBase.db")
    cmd = "SELECT * FROM People WHERE Id = "+str(Id)
    cursor = conn.execute(cmd)
    '''isRecordExit = 0
    for row in cursor:
        isRecordExit = 1
    if isRecordExit == 1:
        cmd = "UPDATE People SET Name = '"+str(Name)+"' WHERE Id = "+str(Id)
    else:'''
    cmd = "INSERT INTO People(Id, Name) Values ("+str(Id)+", '"+str(Name)+"')"
    conn.execute(cmd)
    conn.commit()
    conn.close()


def capImage(request):
    #return HttpResponse('''<h1>form</h1> ''')
    
    #id = input("enter the Id")
    #name = input("enter the name")

    #insertOrUpdate(id, name)
    #print(request.GET.get("capImage"))
    '''if request.GET.get("training"):
        print '11'
        tr = training()'''

    if request.GET.get("capImage"):
        #print(request)
        #print('nav')
        sampleNumber = 0
        faceDetect = cv2.CascadeClassifier('/media/navneet/72f83045-b7eb-4237-a111-1f6156ea4496/django/pro1/polls/haarcascade_frontalface_default.xml')
        cam = cv2.VideoCapture(0)
        while (True):
            #return render(request, 'ai.html',)
            #print('1')
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #print('3')
            faces = faceDetect.detectMultiScale(gray, 1.3, 5)
            #print('2')
            for (x, y, w, h) in faces:
                sampleNumber = sampleNumber+1
                cv2.imwrite("ImageColl/1."+str(sampleNumber)+".jpg",
                            gray[y:y+h, x:x+w])
                cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 2)
                cv2.waitKey(100)
            cv2.imshow("face", img)
            cv2.waitKey(1)
            if (sampleNumber>20):
                break
        cam.release()
        cv2.destroyAllWindows()
        return render(request, 'capImage.html',)
      

    if request.GET.get("training"):
        #print nav3
        
        print('nav2')
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
        except Exception as e:
            print(e)
            pass
        path = 'ImageColl'
        print('nav')

        def getImageWithId(path):
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

            faces = []
            Ids = []
            for imagepath in imagePaths:
                faceImg = Image.open(imagepath).convert('L')
                faceNp = np.array(faceImg, 'uint8')
                ID = int(os.path.split(imagepath)[-1].split('.')[1])
                faces.append(faceNp)
                print (ID)
                Ids.append(ID)
                cv2.imshow("training", faceNp)
                cv2.waitKey(10)
            return Ids, faces
        Ids, faces = getImageWithId(path)
        print('333')
        recognizer.train(faces, np.array(Ids))
        print('111')
        recognizer.save('trainingData.yml')
        print('222')
        cv2.destroyAllWindows()
        return render(request, 'capImage.html',)
    #else:
    if request.GET.get("testImage"):
        faceDetect = cv2.CascadeClassifier('/media/navneet/72f83045-b7eb-4237-a111-1f6156ea4496/django/pro1/polls/haarcascade_frontalface_default.xml')
        cam = cv2.VideoCapture(0)
        rec = cv2.face.LBPHFaceRecognizer_create()
        rec.read('trainingData.yml')

        font = cv2.FONT_HERSHEY_SIMPLEX

        def getProfile(id):
            conn = sqlite3.connect("FaceBase.db")
            cmd = "SELECT *FROM People WHERE Id = "+str(id)
            cursor = conn.execute(cmd)
            profile = None
            for row in cursor:
                profile = row
            conn.close()
            return profile
                

        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceDetect.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 2)
                id, conf = rec.predict(gray[y:y+h, x:x+w])

                #profile = getProfile(id)
                profile = ['Navneet','a','b','c']
                if( profile != None):
                    cv2.putText(img, str(profile[0]), (x, y+h+30), font, 1.0, 255, 2)
                    
                    cv2.putText(img, str(profile[1]), (x, y+h+60), font, 1.0, 255, 2)
                    
                    cv2.putText(img, str(profile[2]), (x, y+h+90), font, 1.0, 255, 2)
                    
                    cv2.putText(img, str(profile[3]), (x, y+h+120), font, 1.0, 255, 2)

                    
                
            cv2.imshow("face", img)

            if cv2.waitKey(33) == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()
        return render(request, 'capImage.html',)


    return render(request, 'capImage.html',)
    

#def testImage(request):

