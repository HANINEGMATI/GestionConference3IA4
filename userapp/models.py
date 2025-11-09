from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import uuid
# Create your models here.
def generate_user_id():
    return "USER"+uuid.uuid4().hex[:4].upper()
def verify_email(email):
    domaine=["esprit.tn","seasame.com","centrale.com","tek up"]
    if email.split("@")[1] not in domaine:
        raise ValidationError("l'email est invalide  et doit appartenir aun demain universitaire privé ")
    # /s c'est pour l'espace et le tiret
name_validator = RegexValidator(
    regex=r'^[a-zA-Z\s\-\']+$', 
    message='Seules les lettres, espaces, tirets et apostrophes sont autorisés.'
)
class User(AbstractUser):
    user_id = models.CharField(max_length=8, unique=True, editable=False, default=generate_user_id)
    first_name = models.CharField(max_length=30, validators=[name_validator])
    last_name = models.CharField(max_length=30, validators=[name_validator])
    affiliation = models.CharField(max_length=100)
    ROLE_CHOICES = [
        ('participant', 'Participant'),
        ('organisateur', 'Organisateur'),
        ('comite', 'Comite'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')
    nationality = models.CharField(max_length=50)
    email = models.EmailField(unique=True, validators=[verify_email])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
