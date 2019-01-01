from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
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
            data = parser.parse(data).date()
        else:
            raise Exception("Nieprawidłowy format daty!")

        wlasciciel = request.POST.get('owner')
        komentarz = request.POST.get('comment')
        pokoj = Room.objects.get(pk=room_id)
        if (data,) in pokoj.reservation_set.filter(date__gte=date.today()).values_list('date'):
            message = "Pokój jest już zarezerwowany w danym terminie."
            return HttpResponseRedirect("/reservation/{}".format(str(room_id)), locals())
        else:
            res = Reservation.objects.create(owner=wlasciciel, date=data, room=pokoj, comment=komentarz)
            return HttpResponseRedirect("/")

class Search(MyView):

    def get(self, request):
        
        nazwa = request.GET.get('name')
        min_miejsc = request.GET.get('seats_min')
        max_miejsc = request.GET.get('seats_max')
        rzutnik = request.GET.get('projector')
        dzien = request.GET.get('day')
        data = parser.parse(dzien).date()
        header_text = "Wolne sale w dniu: {}".format(dzien)

        rooms = Room.objects.all().order_by('seats')

        if nazwa:
            rooms = rooms.filter(name=nazwa)
        if min_miejsc:
            rooms = rooms.filter(seats__gte=min_miejsc)
        if max_miejsc:
            rooms = rooms.filter(seats__lte=max_miejsc)
        if rzutnik:
            rooms = rooms.filter(projector=True)
        
        for room in rooms:
            if (data,) in room.reservation_set.all().values_list('date'):
                rooms = rooms.exclude(pk=room.id)

        return render(request, 'search.html', locals())