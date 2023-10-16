from django.shortcuts import render, redirect
from .forms import RoomSelectionForm, CreateRoomForm
from .models import Chatrooms


def index(request):
    chatrooms = Chatrooms.objects.all()
    room_list = [(room.name, room.name) for room in chatrooms]
    if request.method == "POST":
        form = RoomSelectionForm(request.POST, room_choices=room_list)
        if form.is_valid():
            selected_room = form.cleaned_data["selected_room"]
            return redirect("room", room_name=selected_room)
    else:
        form = RoomSelectionForm(room_choices=room_list)
    return render(request, "realchat/index.html", {"form": form})


def room(request, room_name):
    return render(request, "realchat/room.html", {"room_name": room_name})


def create_room(request):
    if request.method == "POST":
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data["name"]
            return redirect("room", room_name=room_name)
    else:
        form = CreateRoomForm()
    return render(request, "realchat/create_room.html", {"form": form})
