from django.urls import path
from . import views

urlpatterns = [
    path('room_page', views.room, name='room'),
    path('home_page', views.home, name='home'),
    path('database_page', views.database, name='database'),
    path('refresh', views.refresh, name='refresh'),
 #   path('database', views.database, name='database'),
]
