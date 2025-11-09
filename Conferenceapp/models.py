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
    submission_id = models.CharField(max_length=20, primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    keywords = models.CharField(
        max_length=200,
        validators=[validate_keywords],
        help_text="Mots-clés séparés par des virgules (maximum 10)"
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ("Submitted", "Submitted"),
            ("Under Review", "Under Review"),
            ("Accepted", "Accepted"),
            ("Rejected", "Rejected"),
        ],
        default="Submitted"
    )
    file = models.FileField(
        upload_to='submissions_pdfs/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        null=True, blank=True
    )
    submission_date = models.DateTimeField(auto_now_add=True)
    payed = models.BooleanField(default=False)
    conference_id = models.ForeignKey('Conference', on_delete=models.CASCADE, related_name='submissions')
    user_id = models.ForeignKey('userapp.User', on_delete=models.CASCADE, related_name='submissions')

    def __str__(self):
        return f"{self.title} ({self.submission_id})"

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
    if not self.user_id:
        return  # Ne rien valider si user_id non défini encore (sera défini dans form_valid)
    
    today = timezone.now().date()
    submissions_today = Submission.objects.filter(
        user_id=self.user_id,
        submission_date__date=today
    ).exclude(pk=self.pk if self.pk else None).count()

    if submissions_today >= 1:
        raise ValidationError("You can submit only once per day.")

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
