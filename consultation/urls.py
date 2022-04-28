from django.urls import path
from . import views

urlpatterns = [
   
#     path('', views.index2, name='index2'),
#     path('laws', views.countrylaws, name='laws'),
#     path('countrylaws', views.laws, name="countrylaws"),
#     path('sitebreach', views.sitebreach, name='sitebreach'),
#     path('analysis', views.analysis, name="analysis"),
#     path('sum', views.sum, name = "sum"),
#     path('search', views.search, name= "search"),
    path('appointment-book', views.appointment_book, name="appointment_book"),
  ]