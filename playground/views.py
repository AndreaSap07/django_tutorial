from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Here we create the request and take the responses. The views.py is a request handler

def say_hello(request):
    """Here we do the magic, we could:
        -Pull data from db
        -Send an email
        -Transform data"""
    return render(request, 'hello.html', {'name': 'Mario'})
