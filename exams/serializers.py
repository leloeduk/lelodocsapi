from rest_framework import serializers
from .models import Exam

class ExamSerializer(serializers.ModelSerializer):
    # If you need backward compatibility with 'type' in API responses:
    type = serializers.CharField(source='exam_type', read_only=True)
    
    class Meta:
        model = Exam
        fields = [
            'id',
            'title',
            'year',
            'subject',
            'exam_type',  # The actual model field
            'type',       # The alias (only include if needed)
            'diploma_type',
            'serie_bac',
            'exam_file',
            'correction_file',
            'is_premium',
            'created_at'
        ]