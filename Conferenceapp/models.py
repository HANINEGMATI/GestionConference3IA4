from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid
from datetime import date

# Create your models here.
def generate_submission_id():
    return "SUB-" + uuid.uuid4().hex[:8].upper()

def validate_keywords(value):
    """Valide que le nombre de mots-clés ne dépasse pas 10"""
    keywords = [kw.strip() for kw in value.split(',') if kw.strip()]
    if len(keywords) > 10:
        raise ValidationError(f"Trop de mots-clés. Maximum 10 autorisés, {len(keywords)} fournis.")

def validate_session_time(start_time, end_time):
    """Valide que l'heure de fin est supérieure à l'heure de début"""
    if end_time <= start_time:
        raise ValidationError("L'heure de fin doit être supérieure à l'heure de début.")
class Conference(models.Model):
    Conference_id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    THEME= [
        ('cs&ai', 'Computer Science & Artificial Intelligence'),
        ("cs", "Computer Science"),
        ("social", "Social Sciences"),
        
    ]
   
    theme=models.CharField(max_length=100, choices=THEME)
    location=models.CharField(max_length=100)
    start_date=models.DateField()
    end_date=models.DateField()
    description=models.TextField(validators=[MinLengthValidator(limit_value=30,message="La description doit contenir au moins 30 caractères.")])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def duration(self):
        """Calcule la durée de la conférence en jours"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1  # +1 pour inclure le dernier jour
        return 0
    duration.short_description = "Durée (jours)"
    
    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")
    
class Submission(models.Model):
    submission_id = models.CharField(max_length=100, primary_key=True , unique=True, editable=False)
    user_id=models.ForeignKey("userapp.User",on_delete=models.CASCADE, related_name='submissions')
    conference_id=models.ForeignKey(Conference, on_delete=models.CASCADE , related_name='submissions')
    title= models.CharField(max_length=100)
    abstract=models.TextField()
    keyword=models.CharField(max_length=200, validators=[validate_keywords], 
                            help_text="Mots-clés séparés par des virgules (maximum 10)")
    paper=models.FileField(upload_to='papers/', 
                          validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
                          help_text="Seuls les fichiers PDF sont autorisés")
    STATUT_choices=[
        ("Submitted","Submitted"),
        ("Under Review","Under Review"),
        ("Accepted","Accepted"),
        ("Rejected","Rejected")]
    status=models.CharField(max_length=20, choices=STATUT_choices, default="Submitted")
    submission_date=models.DateTimeField(auto_now_add=True)
    payed = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Générer submission_id seulement lors de la création
        if getattr(self, "_state", None) is not None and getattr(self._state, "adding", False):
            if not self.submission_id:
                new_id = generate_submission_id()
                while Submission.objects.filter(submission_id=new_id).exists():
                    new_id = generate_submission_id()
                self.submission_id = new_id
        super().save(*args, **kwargs)
    
    def clean(self):
        # Vérifier que la conférence est à venir par rapport à la date de soumission
        if self.conference_id and self.submission_date:
            submission_date_only = self.submission_date.date()  # Extraire seulement la date
            if self.conference_id.start_date <= submission_date_only:
                raise ValidationError("Les soumissions ne peuvent être faites que pour des conférences à venir.")
        
        # Limiter le nombre de soumissions par utilisateur par jour (max 3)
        try:
            if self.user_id_id:  # Vérifier directement l'ID
                today = date.today()
                submissions_today = Submission.objects.filter(
                    user_id_id=self.user_id_id,
                    created_at__date=today
                ).exclude(pk=self.pk if self.pk else None).count()
                
                if submissions_today >= 3:
                    raise ValidationError("Un utilisateur ne peut faire que 3 soumissions maximum par jour.")
        except (AttributeError, ValueError):
            # Ignorer la validation si l'utilisateur n'est pas encore défini
            pass
        
        # example usage — adjust to your actual validation logic
        if hasattr(self, 'submission_date') and self.submission_date and self.submission_date > date.today():
            raise ValidationError("La date de soumission ne peut pas être dans le futur.")
    
class Organizing_commiteee(models.Model):
    # committee_id = models.AutoField(primary_key=True)
    user_id=models.ForeignKey("userapp.User",on_delete=models.CASCADE, related_name='committees')
    conference_id=models.ForeignKey(Conference, on_delete=models.CASCADE , related_name='committees')
    ROLE_CHOICES=[
        ("Chair","Chair"),
        ("Co-Chair","Co-Chair"),
        ("Member","Member")
        ]
    role=models.CharField(max_length=100, choices=ROLE_CHOICES)
    date_joined=models.DateField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
