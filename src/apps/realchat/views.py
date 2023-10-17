from django.shortcuts import redirect
from .forms import RoomSelectionForm, CreateRoomForm
from .models import Chatrooms
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)


class IndexView(FormView):
    template_name = "realchat/index.html"
    form_class = RoomSelectionForm
    success_url = reverse_lazy("room")

    def form_valid(self, form):
        selected_room = form.cleaned_data["selected_room"]
        return redirect("room", room_name=selected_room)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        chatrooms = Chatrooms.objects.all()
        room_list = [(room.name, room.name) for room in chatrooms]
        form_kwargs["room_choices"] = room_list
        return form_kwargs


class RoomView(TemplateView):
    template_name = "realchat/room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_name"] = self.kwargs["room_name"]
        return context


class CreateRoomView(FormView):
    template_name = "realchat/create_room.html"
    form_class = CreateRoomForm

    def form_valid(self, form):
        room_name = form.cleaned_data["name"]
        Chatrooms.objects.create(name=room_name)
        logger.info(f'The user {self.request.user.username} has created the room "{room_name}"')
        return redirect("room", room_name=room_name)

    def get_success_url(self):
        return reverse_lazy("room", kwargs={"room_name": self.kwargs["room_name"]})
