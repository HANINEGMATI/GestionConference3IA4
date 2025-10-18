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
    user_id = models.CharField(max_length=8, primary_key=True, unique=True, editable=False)
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
    # args narefch 9edeh min argument chnab3eth form tuple
    # args avec clé de forme dictionnaire
    def save(self, *args, **kwargs):
        # Ne générer un user_id que lors de la création de l'objet (self._state.adding)
        # Evite de modifier la clé primaire lors d'appels à save(update_fields=[...])
        if getattr(self, "_state", None) is not None and getattr(self._state, "adding", False):
            if not self.user_id:
                new_id = generate_user_id()
                # Boucle de sécurité pour éviter les collisions
                while User.objects.filter(user_id=new_id).exists():
                    new_id = generate_user_id()
                self.user_id = new_id
        super().save(*args, **kwargs)
    
    # submissions = models.ManyToManyField('Conferenceapp.Conference', through='Submission', related_name='submitted_users')
    # organizing_committees = models.ManyToManyField('Conferenceapp.Conference', through='Organizing_committeee', related_name='organizers')

