from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Your account has been created! You are now able to login!"
            )
            return redirect("login")
    else:
        form = UserCreationForm(request.POST)
    return render(request, "users/register.html", {"form": form})
