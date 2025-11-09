from django.contrib import admin
from .models import Conference, Submission, Organizing_commiteee
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Submission
# === Personnalisation globale de l’interface admin ===
admin.site.site_header = "Gestion des conférences"
admin.site.site_title = "Administration des conférences"
admin.site.index_title = "Bienvenue dans l'administration des conférences"

# === Inline Submission (Stacked) ===
class SubmissionStackedInline(admin.StackedInline):
    model = Submission
    readonly_fields = ('submission_id', 'submission_date')
    extra = 0
    max_num = 10
    fieldsets = (
        ('Informations de base', {
            'fields': ('user_id', 'title', 'abstract', 'keywords')
        }),
        ('Fichier et statut', {
            'fields': ('file', 'status', 'payed')
        }),
        ('Métadonnées', {
            'fields': ('submission_id', 'submission_date'),
            'classes': ('collapse',)
        }),
    )

# === Inline Submission (Tabular) ===
class SubmissionTabularInline(admin.TabularInline):
    model = Submission
    fields = ('title', 'status', 'user_id', 'payed')
    readonly_fields = ('submission_id', 'submission_date')
    extra = 0
    max_num = 5

# === Configuration admin pour Conference ===
@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme', 'location', 'start_date', 'end_date', 'duration')
    list_filter = ('theme', 'location', 'start_date')
    search_fields = ('name', 'description', 'location')
    ordering = ('start_date',)
    date_hierarchy = 'start_date'
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'theme', 'description')
        }),
        ('Logistique', {
            'fields': ('location', 'start_date', 'end_date')
        }),
    )
    inlines = [SubmissionStackedInline]  # ou SubmissionTabularInline

    def duration(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return "-"
    duration.short_description = "Durée (jours)"

# === Configuration admin pour Submission ===
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'user_id', 'conference_id', 'submission_date', 'payed', 'short_abstract')
    list_filter = ('status', 'payed', ('conference_id', admin.RelatedOnlyFieldListFilter), 'submission_date')
    search_fields = ('title', 'keywords', 'user_id__username')
    list_editable = ('status', 'payed')
    readonly_fields = ('submission_id', 'submission_date')
    fieldsets = (
        ('Infos générales', {
            'fields': ('submission_id', 'title', 'abstract', 'keywords')
        }),
        ('Fichier et conférence', {
            'fields': ('file', 'conference_id')
        }),
        ('Suivi', {
            'fields': ('status', 'payed', 'submission_date', 'user_id')
        }),
    )

    actions = ['mark_as_paid', 'accept_submissions']

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(payed=True)
        self.message_user(request, f"{updated} soumission(s) marquée(s) comme payée(s).")
    mark_as_paid.short_description = "Marquer les soumissions sélectionnées comme payées"

    def accept_submissions(self, request, queryset):
        updated = queryset.update(status='Accepted')
        self.message_user(request, f"{updated} soumission(s) acceptée(s).")
    accept_submissions.short_description = "Accepter les soumissions sélectionnées"

    def short_abstract(self, obj):
        text = obj.abstract or ""
        return (text[:50] + "...") if len(text) > 50 else text
    short_abstract.short_description = "Résumé court"

# === Configuration admin pour Organizing Committee ===
@admin.register(Organizing_commiteee)
class OrganizingCommitteeAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'conference_id', 'role', 'date_joined')
    list_filter = ('role', 'conference_id', 'date_joined')
    search_fields = ('user_id__username', 'user_id__email', 'conference_id__name')
