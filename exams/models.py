from django.db import models

class Exam(models.Model):
    # Types d'examens (Rouge/Blanc)
    EXAM_TYPE_CHOICES = [
        ('rouge', 'Rouge'),
        ('blanc', 'Blanc'),
    ]
    
    # Diplômes nationaux
    DIPLOMA_TYPE_CHOICES = [
        ('none', 'Aucun diplôme'),
        ('bepec', 'BEPC'),
        ('bac', 'Baccalauréat'),
    ]

    # Séries pour le Bac
    SERIE_BAC_CHOICES = [
        ('A', 'Série A'),
        ('C', 'Série C'),
        ('D', 'Série D'),
        ('E', 'Série E'),
        ('F', 'Série F'),
        ('F1', 'Série F1'),
        ('F2', 'Série F2'),
        ('F3', 'Série F3'),
        ('F4', 'Série F4'),
        ('H', 'Série H'),
        ('G', 'Série G'),
        ('TI', 'Série TI'),
        ('autre', 'Autre série'),
    ]

    # Champs principaux
    id = models.CharField(primary_key=True, max_length=50, editable=False)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    subject = models.CharField(max_length=100)
    
    # Type d'examen (obligatoire)
    exam_type = models.CharField(max_length=100, choices=EXAM_TYPE_CHOICES)
    
    # Diplôme associé (optionnel)
    diploma_type = models.CharField(
        max_length=100,
        choices=DIPLOMA_TYPE_CHOICES,
        default='none'
    )
    
    # Série (uniquement si Bac)
    serie_bac = models.CharField(
        max_length=10,
        choices=SERIE_BAC_CHOICES,
        blank=True,
        null=True,
        help_text="Renseigné uniquement si diplôme = Bac"
    )
    
    # Fichiers
    exam_file = models.FileField(upload_to='uploads/%Y/%m/')
    correction_file = models.FileField(upload_to='uploads/%Y/%m/', blank=True, null=True)
    
    # Métadonnées
    is_premium = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.year})"

    def save(self, *args, **kwargs):
        if not self.id:
            # Génération de l'ID selon le type
            if self.diploma_type == 'bac':
                prefix = f"BAC-{self.serie_bac}"
            elif self.diploma_type == 'bepec':
                prefix = "BEPC"
            else:
                prefix = f"{self.exam_type[0].upper()}"  # R pour Rouge, B pour Blanc
            
            # Base commune
            base_id = f"{prefix}-{self.subject[:4].upper()}-{self.year}"
            
            # Compteur pour éviter les doublons
            existing_exams = Exam.objects.filter(id__startswith=base_id).count()
            self.id = f"{base_id}-{str(existing_exams + 1).zfill(3)}"

        super().save(*args, **kwargs)

    def clean(self):
        """Validation supplémentaire"""
        if self.diploma_type == 'bac' and not self.serie_bac:
            raise ValidationError("La série doit être renseignée pour le Bac")
        if self.serie_bac and self.diploma_type != 'bac':
            raise ValidationError("La série ne peut être renseignée que pour le Bac")