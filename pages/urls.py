from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('home/', views.home_view), #I am not calling the function 'say_hello' NO NEED TO PUT THE PARENTHESIS!!!
    path('about/', views.about_view) #I am not calling the function 'say_hello' NO NEED TO PUT THE PARENTHESIS!!!


]