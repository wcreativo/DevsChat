from django.urls import path

from .views import IndexView, RoomView, CreateRoomView


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("devs/create/", CreateRoomView.as_view(), name="create"),
    path("<str:room_name>/", RoomView.as_view(), name="room"),
]
