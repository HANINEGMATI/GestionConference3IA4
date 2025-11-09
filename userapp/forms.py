from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'affiliation',
            'nationality',
            'password1',
            'password2'
        ]
        labels = {
            'username': 'Nom d’utilisateur',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Adresse email',
            'affiliation': 'Affiliation',
            'nationality': 'Nationalité',
            'password1': 'Mot de passe',
            'password2': 'Confirmer mot de passe',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "participant"  # Défini automatiquement
        if commit:
            user.save()
        return user
