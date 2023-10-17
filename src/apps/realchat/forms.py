from django import forms
from django.core.validators import RegexValidator

name_validator = RegexValidator(
    regex=r"^[A-Za-z0-9_-]+$",
    message="Name can only contain letters, numbers, _, and -",
)


class RoomSelectionForm(forms.Form):
    selected_room = forms.ChoiceField(choices=(), widget=forms.Select())

    def __init__(self, *args, **kwargs):
        room_choices = kwargs.pop("room_choices", [])
        super(RoomSelectionForm, self).__init__(*args, **kwargs)
        self.fields["selected_room"].choices = room_choices


class CreateRoomForm(forms.Form):
    name = forms.CharField(max_length=255, validators=[name_validator])
