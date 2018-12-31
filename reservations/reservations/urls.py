"""reservations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from booking.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', AllRooms.as_view(), name='home'),
    path('room/new', AddNewRoom.as_view(), name='new-room'),
    path('room/modify/<int:id>', ModifyRoom.as_view(), name='modify-room'),
    path('room/delete/<int:id>', DeleteRoom.as_view(), name='delete-room'),
    path('room/<int:id>', RoomDetails.as_view(), name='room-details'),
    path('reservation/<int:room_id>', Reserve.as_view(), name='reservation'),
    path('search', Search.as_view(), name='search'),

]
