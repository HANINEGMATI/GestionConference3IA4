from django.shortcuts import render, redirect
from django.contrib.auth import logout  # <-- garde bien CET import ici
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'participant'
            user.save()
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "userapp/register.html", {"form": form})  # <-- attention au chemin complet


def logout_view(request):
    logout(request)  # <-- maintenant cette fonction est bien reconnue
    return redirect("login")
