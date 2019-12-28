# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def contact(request):
    return HttpResponse('''
                        
                            <button name="button" type="button" onclick="window.location.href='http://127.0.0.1:8000/home' ">home</button>
                            <button name="button" type="button" onclick="window.location.href='http://127.0.0.1:8000/about' ">about us</button>
                            <button name="button" type="button" onclick="window.location.href='http://127.0.0.1:8000/contact' ">contact</button>
                            <button name="button" type="button" onclick="window.location.href='http://127.0.0.1:8000/branch' ">branch</button>
                            <button name="button" type="button" onclick="window.location.href='http://127.0.0.1:8000/form' ">form</button>  
                            <h1>contact</h1> 
                        ''')