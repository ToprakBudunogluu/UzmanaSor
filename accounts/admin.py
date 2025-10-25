from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    # 1. LİSTEDE GÖRÜNECEK ALANLAR (list_display)
    list_display = (
        'username', 
        'email', 
        'user_type',
        'academic_rank',  # <-- BURAYA EKLENDİ
        'is_staff'
    )

    # 2. DÜZENLEME FORMUNDAKİ ALANLAR (fieldsets)
    # Orijinal 'fieldsets'i alıp, üstüne kendi alanlarımızı ekliyoruz
    fieldsets = UserAdmin.fieldsets + (
        ('Proje Özel Alanlari', {
            'fields': (
                'user_type', 
                'academic_rank'   # <-- BURAYA EKLENDİ
            ),
        }),
    )

    # 3. YENİ KULLANICI EKLEME FORMUNDAKİ ALANLAR (add_fieldsets)




    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': (
                'user_type', 
                'academic_rank'   # <-- BURAYA EKLENDİ
            ),
        }),
    )

