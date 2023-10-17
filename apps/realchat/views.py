from django.shortcuts import render
from django.shortcuts import render


def index(request):
    return render(request, "realchat/index.html")


def room(request, room_name):
    return render(request, "realchat/room.html", {"room_name": room_name})
