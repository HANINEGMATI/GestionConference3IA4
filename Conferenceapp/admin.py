from django.contrib import admin
from .models import Conference, Submission, Organizing_commiteee

# === Personnalisation globale de l’interface admin ===
admin.site.site_header = "Gestion des conférences"
admin.site.site_title = "Administration des conférences"
admin.site.index_title = "Bienvenue dans l'administration des conférences"

# === Inline pour Submission (mode Stacked) ===
class SubmissionStackedInline(admin.StackedInline):
    model = Submission
    readonly_fields = ('submission_id', 'submission_date')
    extra = 0  # Ne pas afficher de formulaires vides
    max_num = 10  # Limite le nombre d'inlines

    fieldsets = (
        ('Informations de base', {
            'fields': ('user_id', 'title', 'abstract', 'keyword')
        }),
        ('Fichier et statut', {
            'fields': ('paper', 'status', 'payed')
        }),
        ('Métadonnées', {
            'fields': ('submission_id', 'submission_date'),
            'classes': ('collapse',)
        }),
    )

# === Inline pour Submission (mode Tabular) ===
class SubmissionTabularInline(admin.TabularInline):
    model = Submission
    fields = ('title', 'status', 'user_id', 'payed')
    readonly_fields = ('submission_id', 'submission_date')
    extra = 0
    max_num = 5

# === Configuration de l’admin pour Conference ===
@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    # a. Colonnes affichées
    list_display = ('name', 'theme', 'location', 'start_date', 'end_date', 'duration')
    
    # b. Méthode personnalisée pour la durée
    def duration(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return "-"
    duration.short_description = "Durée (jours)"
    
    # d. Filtres
    list_filter = ('theme', 'location', 'start_date')
    
    # e. Recherche
    search_fields = ('name', 'description', 'location')
    
    # f. Organisation du formulaire par sections
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'theme', 'description')
        }),
        ('Logistique', {
            'fields': ('location', 'start_date', 'end_date')
        }),
    )
    
    # g. Ordering
    ordering = ('start_date',)
    
    # h. Date hierarchy
    date_hierarchy = 'start_date'
    
    # i. Inline Submission
    inlines = [SubmissionStackedInline]  # Remplacer par SubmissionTabularInline si souhaité

# === Configuration pour Submission ===
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'user_id', 'conference_id', 'submission_date', 'payed', 'short_abstract')

    # Utiliser le champ relationnel exact présent dans le modèle (ici 'conference_id')
    list_filter = ('status', 'payed', ('conference_id', admin.RelatedOnlyFieldListFilter), 'submission_date')
    search_fields = ('title', 'keyword', 'user_id__username')

    list_editable = ('status', 'payed')
    readonly_fields = ('submission_id', 'submission_date')
    
    fieldsets = (
        ('Infos générales', {
            'fields': ('submission_id', 'title', 'abstract', 'keyword')
        }),
        ('Fichier et conférence', {
            'fields': ('paper', 'conference_id')
        }),
        ('Suivi', {
            'fields': ('status', 'payed', 'submission_date', 'user_id')
        }),
    )
    
    # Actions personnalisées (méthodes de la classe)
    actions = ['mark_as_paid', 'accept_submissions']

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(payed=True)
        self.message_user(request, f"{updated} soumission(s) marquée(s) comme payée(s).")
    mark_as_paid.short_description = "Marquer les soumissions sélectionnées comme payées"

    def accept_submissions(self, request, queryset):
        updated = queryset.update(status='accepted')  # Assurez-vous que le champ status a cette valeur possible
        self.message_user(request, f"{updated} soumission(s) acceptée(s).")
    accept_submissions.short_description = "Accepter les soumissions sélectionnées"

    def short_abstract(self, obj):
        text = obj.abstract or ""
        return (text[:50] + "...") if len(text) > 50 else text
    short_abstract.short_description = "Résumé court"

# === Configuration pour Organizing Committee ===
@admin.register(Organizing_commiteee)
class OrganizingCommitteeAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'conference_id', 'role', 'date_joined')
    list_filter = ('role', 'conference_id', 'date_joined')
    search_fields = ('user_id__username', 'user_id__email', 'conference_id__name')
