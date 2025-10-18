#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionConference.settings')
django.setup()

from userapp.models import User

print("=== UTILISATEURS EXISTANTS ===")
users = User.objects.all()
for user in users:
    print(f"""
Nom d'utilisateur: {user.username}
Email: {user.email}
Prénom: {user.first_name}
Nom: {user.last_name}
Superuser: {user.is_superuser}
Actif: {user.is_active}
User ID: {user.user_id}
---""")

print(f"\nTotal: {users.count()} utilisateur(s)")