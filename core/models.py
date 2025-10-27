from django.db import models
from django.conf import settings


class CourseTest(models.Model):
    course_teacher = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Hoca silinirse, derslik SİLİNMEZ, hoca alanı BOŞA DÜŞER.
        null=True,      
        blank=True           # Veritabanında bu alanın boş olmasına izin ver.
    )
    course_code = models.CharField(max_length=20,  verbose_name="Ders Kodu", null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name="Ders Basligi")
    description = models.TextField(verbose_name="Ders Aciklamasi", null=True, blank=True, )
    
    def __str__(self):
        return f"{self.title} - {self.course_teacher.username}"

class ClassTermTest(models.Model):

    class_name = models.CharField(
        max_length=100, 
        verbose_name="Derslik Adi",
        )
    
    def __str__(self):
        return f"{self.class_name}"
    
class QuestionBinderTest(models.Model):

    title = models.CharField(max_length=255, verbose_name="Soru Başlığı")
    content = models.TextField(verbose_name="Soru İçeriği")
    created_at = models.DateTimeField(auto_now_add=True)
    
    question_author= models.ForeignKey(settings.AUTH_USER_MODEL , related_name= 'Sorunun_Sahibi', verbose_name='Sorunun Sahibi', on_delete=models.CASCADE)
    question_current_handler= models.ForeignKey(settings.AUTH_USER_MODEL , verbose_name='Sorunun Su Anki Sorumlusu', on_delete=models.CASCADE)
    question_old_handler= models.ForeignKey(settings.AUTH_USER_MODEL , related_name= 'Sorunun_Eski_Sorumlusu' , verbose_name='Sorunun Eski Sorumlusu', null=True, blank=True, on_delete=models.SET_NULL)
    question_priority = models.IntegerField( max_length=10 , verbose_name='Onem Sirasi' , editable=False)
    class_term = models.ForeignKey(ClassTermTest , verbose_name="Bolum ve Donem" , on_delete=models.CASCADE)
    course = models.ForeignKey(CourseTest , verbose_name="Ana Ders", on_delete=models.CASCADE)

    
    def save(self, *args, **kwargs):
 
        if self.question_author.academic_rank == 4:   
            self.question_priority = 5
        elif self.question_author.academic_rank == 3:
            self.question_priority = 4
        elif self.question_author.academic_rank == 2: 
            self.question_priority = 3
        elif self.question_author.user_type == 'r_student':   
            self.question_priority = 2
        else:
            self.question_priority = 1

        super().save(*args, **kwargs)


# MODEL 4: CEVAP (Hiçbir değişiklik yok, zaten Soru'ya bağlıydı)
class Answer(models.Model):
    question = models.ForeignKey(
        QuestionBinderTest, 
        on_delete=models.CASCADE, 
        related_name='answers', 
        verbose_name="Soru"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="Cevaplayan"
    )
    content = models.TextField(verbose_name="Cevap Icerigi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cevap: {self.question.title[:30]}..."
