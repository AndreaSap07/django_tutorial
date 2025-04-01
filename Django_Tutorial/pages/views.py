from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Here we create the request and take the responses. The views.py is a request handler

def home_view(request, *args, **kwargs):
    """Here we do the magic, we could:
        -Pull data from db
        -Send an email
        -Transform data"""
    return render(request, 'home.html', {}) #render(request, 'hello.html', {'name': 'Mario'})

def about_view(request, *args, **kwargs):

    return render(request, 'about.html', {}) 