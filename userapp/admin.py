from django.contrib import admin
from .models import User
from Sessionapp.models import Session

admin.site.register(User)
admin.site.register(Session)
