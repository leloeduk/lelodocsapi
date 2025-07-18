from django.contrib import admin
from .models import Exam
# Register your models here.
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'subject', 'niveau', 'type', 'is_premium', 'created_at')
    list_filter = ('year', 'type', 'niveau', 'is_premium', 'subject')
    search_fields = ('title', 'subject', 'type', 'niveau')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

