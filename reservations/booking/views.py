from django.shortcuts import render, redirect
from django.views import View
from booking.models import Room


class AllRooms(View):

    def get(self, request):
        rooms = Room.objects.all()
        return render(request, 'all_rooms.html', {'rooms': rooms})
    
    def post(self, request):
        rooms = Room.objects.all()
        return render(request, 'all_rooms.html')


class AddNewRoom(View): 

    def get(self, request):
        return render(request, 'add_room.html')
    
    def post(self, request):
        nazwa = request.POST.get('name')
        pietro = request.POST.get('floor')
        miejsca = request.POST.get('seats')
        rzutnik = request.POST.get('projector')
        biurka = request.POST.get('desks')
        if rzutnik:
            rzutnik = True
        else:
            rzutnik = False
        if biurka:
            biurka = True
        else:
            biurka = False
        room = Room.objects.create(name=nazwa, floor=pietro, seats=miejsca, projector=rzutnik, desks=biurka)
        return redirect("/")


class ModifyRoom(View):
    pass


class DeleteRoom(View):
    pass


class RoomDetails(View):
    pass
