from django.contrib import admin
from .models import Exam
from django import forms

class ExamAdminForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        diploma_type = cleaned_data.get('diploma_type')
        serie_bac = cleaned_data.get('serie_bac')
        
        if diploma_type == 'bac' and not serie_bac:
            raise forms.ValidationError("La série doit être renseignée pour le Bac")
        if serie_bac and diploma_type != 'bac':
            raise forms.ValidationError("La série ne peut être renseignée que pour le Bac")
        return cleaned_data

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    form = ExamAdminForm
    list_display = ('title', 'year', 'subject', 'exam_type', 'diploma_type', 'serie_bac', 'is_premium', 'created_at')
    list_filter = (
        'year',
        'exam_type',
        'diploma_type',
        'serie_bac',
        'is_premium',
        'subject'
    )
    search_fields = ('title', 'subject', 'exam_type', 'diploma_type')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'id')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'year', 'subject')
        }),
        ('Type', {
            'fields': ('exam_type', 'diploma_type', 'serie_bac')
        }),
        ('Fichiers', {
            'fields': ('exam_file', 'correction_file')
        }),
        ('Métadonnées', {
            'fields': ('is_premium', 'created_at', 'id')
        }),
    )
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.diploma_type != 'bac':
            # Cache le champ série si pas un Bac
            fieldsets = list(fieldsets)
            fieldsets[1] = ('Type', {
                'fields': ('exam_type', 'diploma_type')
            })
        return fieldsets