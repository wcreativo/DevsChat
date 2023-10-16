from django import forms


class RoomSelectionForm(forms.Form):
    selected_room = forms.ChoiceField(choices=(), widget=forms.Select())

    def __init__(self, *args, **kwargs):
        room_choices = kwargs.pop("room_choices", [])
        super(RoomSelectionForm, self).__init__(*args, **kwargs)
        self.fields["selected_room"].choices = room_choices
