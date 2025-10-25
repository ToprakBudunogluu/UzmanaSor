from django.db import models
from django.conf import settings

# MODEL 1: ANA DERS (Katalogdaki ders)
class Course(models.Model):
    course_code = models.CharField(max_length=20,  verbose_name="Ders Kodu", null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name="Ders Basligi")
    description = models.TextField(blank=True, verbose_name="Ders Aciklamasi")
    
    def __str__(self):
        return f"{self.course_code} - {self.title}"


# MODEL 2: AÇILAN DERS / DERSLİK (Hocayı ve Dersi birleştiren model)
# Bu model, bir "Course"u bir "Teacher"a ve bir "Dönem"e bağlar.
class Class(models.Model):
    course = models.ForeignKey(
        Course, 
        on_delete=models.SET_NULL, # Ana Ders (CS101) katalogdan silinirse, derslik SİLİNMEZ, ders alanı BOŞA DÜŞER.
        null=True,                 # Veritabanında bu alanın boş olmasına izin ver.
        blank=True,                # Admin panelinde burayı boş bırakmaya izin ver.
        verbose_name="Ana Ders"
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Hoca silinirse, derslik SİLİNMEZ, hoca alanı BOŞA DÜŞER.
        null=True,                 # Veritabanında bu alanın boş olmasına izin ver.
        blank=True,                # Admin panelinde burayı boş bırakmaya izin ver.
        limit_choices_to={'user_type': 'teacher'},
        verbose_name="Dersi Veren Hoca"
    )
    class_name = models.CharField(
        max_length=100, 
        verbose_name="Derslik Adi",
        )
    

    def __str__(self):
        teacher_name = self.teacher.username if self.teacher else "Atanmadi"
        
        try: 
            if self.course.course_code != None and teacher_name != None :
                return f"{self.course.course_code} ({self.class_name}) - {teacher_name}"
            else:
                return f"{self.class_name}"
        except AttributeError:
            return f"{self.class_name}"


class Question(models.Model):
    # Bu alanlar aynı
    offering = models.ForeignKey(
        Class, 
        on_delete=models.CASCADE, 
        related_name='questions',
        verbose_name="Açılan Ders",
        null=True,
        blank=True
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        #limit_choices_to={'user_type': 'student'},
        related_name='questions',
        verbose_name="Soruyu Soran"
    )

    current_handler = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'user_type': 'teacher'},
        verbose_name="Mevcut Sorumlu (Hoca)",
        help_text="Soruyu yanıtlaması beklenen hoca."
    )

    old_handler = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Hoca silinse bile 'eski' kaydı kalsın
        null=True,
        blank=True,
        related_name='handled_by_me_previously', # Gelişmiş bir 'reverse' isim
        verbose_name="Önceki Sorumlu (Hoca)"
    )

    priority = models.IntegerField(
        default=1,
        verbose_name="Önem Sırası",
        editable=False
    )

    title = models.CharField(max_length=255, verbose_name="Soru Başlığı")
    content = models.TextField(verbose_name="Soru İçeriği")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        

        if self.author.academic_rank == 4:   
            self.priority = 5
        elif self.author.academic_rank == 3:
            self.priority = 4
        elif self.author.academic_rank == 2: 
            self.priority = 3
        elif self.author.user_type == 'r_student':   
            self.priority = 2
        else:
            self.priority = 1
        

        # --- BÖLÜM B: "HANDLER" (SORUMLU) ATAMA ---
        # Bu logic, sorunun kime gideceğini belirler.
        # Sadece 'yeni' bir soruysa (if not self.pk) ve 'handler'ı boşsa...
        if not self.pk and not self.current_handler:
            # ...ve soru bir dersliğe (offering) bağlıysa...
            if self.offering and self.offering.teacher:
                # ...soruyu o dersliğin hocasına ata.
                self.current_handler = self.offering.teacher

        super().save(*args, **kwargs)
    

# MODEL 4: CEVAP (Hiçbir değişiklik yok, zaten Soru'ya bağlıydı)
class Answer(models.Model):
    question = models.ForeignKey(
        Question, 
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
