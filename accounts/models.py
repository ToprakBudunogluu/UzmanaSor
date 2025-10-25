from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Öğrenci'),
        ('r_student', 'Öğrenci Temsilcisi'),
        ('teacher', 'Öğretmen'),
    )
    



    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES,
        default='student',
        verbose_name='Kullanici Tipi'
    )


    ACADEMIC_RANK_CHOICES = (
        (1, 'Öğrenci Temsilcisi'),  # Öğrenci Temsilcisi
        (2, 'Akademisyen'),         # Normal Öğretim Üyesi
        (3, 'Dekan Yardımcısı'),    # Dekan Yardımcısı
        (4, 'Dekan'),               # Dekan
    )

    
    
    
    academic_rank = models.IntegerField(
        choices=ACADEMIC_RANK_CHOICES,
        default=1,
        verbose_name="Akademik Mertebe",
        null=True,  # Bu alanın veritabanında 'boş' (NULL) olmasına izin ver
        blank=True,  # Bu alanın formlarda 'boş' bırakılmasına izin ver
        
        
    )





    def save(self, *args, **kwargs):
        if self.user_type == 'student':
            self.academic_rank = None
        if self.user_type == 'r_student':
            self.academic_rank = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    