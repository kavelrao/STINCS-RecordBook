from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dataEntry/', views.dataEntry, name='dataEntry'),
    path('designs/', views.designs, name='designs'),
    path('team/', views.team, name='team'),
    path('launches/', views.launches, name='launches'),
]
