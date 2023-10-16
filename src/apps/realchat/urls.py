from django.urls import path

from .views import index, room, create_room


urlpatterns = [
    path("", index, name="index"),
    path("devs/create/", create_room, name="create"),
    path("<str:room_name>/", room, name="room"),
]
