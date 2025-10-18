from django import forms
from .models import Conference

class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['name', 'location', 'start_date', 'end_date', 'description']

        # Labels explicites pour chaque champ
        labels = {
            'name': 'Titre de la conférence',
            'location': 'Lieu',
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'description': 'Description',
        }

        # Widgets personnalisés avec placeholders et types adaptés
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Entrez le titre de la conférence'}),
            'location': forms.TextInput(attrs={'placeholder': 'Entrez le lieu'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'placeholder': 'Entrez la description', 'rows': 4}),
        }
