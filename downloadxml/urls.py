from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('downloadpage/', views.download_page_view, name='download_page'),
    path('downloadGEOV/', views.dl_geov_view, name='dl_geov_view'), #I am not calling the function 'say_hello' NO NEED TO PUT THE PARENTHESIS!!!
        path('filter/', views.filter_page_view, name='filter_page'),
    path('export-csv/', views.export_csv_view, name='export_csv'),

]