from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('product/detail/', views.product_detail_view), #I am not calling the function 'say_hello' NO NEED TO PUT THE PARENTHESIS!!!
    path('product/product_create/', views.product_create_view), #I am not calling the function 'say_hello' NO NEED TO PUT THE PARENTHESIS!!!


]