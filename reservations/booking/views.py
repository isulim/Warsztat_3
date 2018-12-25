from django.shortcuts import render, redirect
from django.views import View
from booking.models import Room


class AllRooms(View):

    def get(self, request):
        rooms = Room.objects.all().order_by('id')
        return render(request, 'all_rooms.html', {'rooms': rooms})

class AddNewRoom(View): 
    
    def get(self, request):
        formname = 'Dodawanie nowej sali'
        return render(request, 'add_room.html', locals())
    
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
    def get(self, request, id):
        formname = 'Modyfikacja danych sali'
        room = Room.objects.get(pk=id)
        return render(request, 'add_room.html', locals())
    
    def post(self, request, id):
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
        
        room = Room.objects.get(pk=id)
        room.name = nazwa
        room.floor = pietro
        room.seats = miejsca
        room.projector = rzutnik
        room.desks = biurka
        room.save()

        return redirect("/")


class DeleteRoom(View):
    def get(self, request, id):
        Room.objects.get(pk=id).delete()
        return redirect("/")



class RoomDetails(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        return render(request, 'room_details.html', {'room': room})