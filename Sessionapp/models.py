from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.
# Validateur pour la salle (lettres et chiffres seulement)
room_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9\s]+$',
    message='Le nom de la salle ne peut contenir que des lettres, chiffres et espaces.'
)
class Session(models.Model):
    Session_id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    topic=models.CharField(max_length=100)
    session_day=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    room=models.CharField(max_length=100, validators=[room_validator],
                          help_text="Nom de la salle (lettres et chiffres seulement)")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    conference=models.ForeignKey('Conferenceapp.Conference', on_delete=models.CASCADE, related_name='sessions')
    
    def clean(self):
        # Vérifier que l'heure de fin est supérieure à l'heure de début
        if self.end_time and self.start_time and self.end_time <= self.start_time:
            raise ValidationError("L'heure de fin doit être supérieure à l'heure de début.")
        
        # Vérifier que la date de session est dans l'intervalle de la conférence
        if self.conference and self.session_day:
            if not (self.conference.start_date <= self.session_day <= self.conference.end_date):
                raise ValidationError(
                    f"La date de session doit être comprise entre {self.conference.start_date} "
                    f"et {self.conference.end_date} (dates de la conférence)."
                )
    