from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('hello/', views.say_hello) #I am not calling the function 'say_hello' NO NEED TO PUT THE PARENTHESIS!!!
]