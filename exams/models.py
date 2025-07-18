from django.db import models

# Create your models here.

class Exam(models.Model):
    TYPE_CHOICES = [
        ('rouge', 'Rouge'),
        ('blanc', 'Blanc'),
    ]

    NIVEAU_CHOICES = [
        ('6e', '6e'),
        ('5e', '5e'),
        ('4e', '4e'),
        ('3e', '3e'),
        ('2nde', '2nde'),
        ('1ère', '1ère'),
        ('Tle', 'Terminale'),
    ]

    id = models.CharField(primary_key=True, max_length=100)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    subject = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES)  # 🆕
    exam_file = models.FileField(upload_to='uploads/%Y/%m/')
    correction_file = models.FileField(upload_to='uploads/%Y/%m/', blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.year})"
