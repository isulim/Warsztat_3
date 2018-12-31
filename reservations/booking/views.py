from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from booking.models import *
from datetime import date
from dateutil import parser


class MyView(View):
    today_str = date.today().strftime("%Y-%m-%d")


class AllRooms(MyView):

    def get(self, request):
        rooms = Room.objects.all().order_by('id')
        dost = ''
        today = date.today()
        today = (today,)

        for room in rooms:
            if today in room.reservation_set.filter(date__gte=date.today()).values_list('date'):
                dost = 'Zajęta'
            else:
                dost = 'Dostępna'
            room.dost = dost
        return render(request, 'all_rooms.html', locals())

class AddNewRoom(MyView): 

    def get(self, request):
        header_text = "Tworzenie nowej sali"
        submit_text = "Dodaj nową salę"
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


class ModifyRoom(MyView):

    def get(self, request, id):
        room = Room.objects.get(pk=id)
        header_text = 'Edycja sali "{}"'.format(room.name)
        submit_text = "Zapisz zmiany"
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


class DeleteRoom(MyView):

    def get(self, request, id):
        Room.objects.get(pk=id).delete()
        return redirect("/")


class RoomDetails(MyView):
  
    def get(self, request, id):
        today = date.today()
        room = Room.objects.get(pk=id)
        reserv = room.reservation_set.filter(date__gte=date.today()).order_by('date')[:30]
        return render(request, 'room_details.html', locals())


class Reserve(MyView):

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        reserv = room.reservation_set.filter(date__gte=date.today()).order_by('date')[:30]
        return render(request, 'reservation_form.html', locals())

    def post(self, request, room_id):
        if request.POST.get('data'):
            data = request.POST.get('data')
        else:
            raise Exception("Nieprawidłowy format daty!")

        wlasciciel = request.POST.get('owner')
        komentarz = request.POST.get('comment')
        pokoj = Room.objects.get(pk=room_id)
        if (parser.parse(data).date(),) in pokoj.reservation_set.filter(date__gte=date.today()).values_list('date'):
            response = HttpResponse("""
            Sala jest już zarezerwowana tego dnia.<br>
            <a href="/">Powrót do głównej</a>
            """)
            return response
        else:
            res = Reservation.objects.create(owner=wlasciciel, date=data, room=pokoj, comment=komentarz)
            return redirect("/")

class Search(MyView):

    def get(self, request):
        header_text = "Wyniki wyszukiwania"
        pass

    def post(self, request):
        nazwa = request.POST.get('name')
        min_miejsc = request.POST.get('seats_min')
        max_miejsc = resuest.POST.get('seats_max')
        rzutnik = request.POST.get('projector')
        dzien = request.POST.get('day')
        data = parser.parse(dzien)

        if dzien:
            rooms = Room.objects.all()
            # filter na obiekcie rooms
        else:
            rooms = "Brak wyników spełniających podane kryteria."