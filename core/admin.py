from django.contrib import admin
from .models import Course, Class, Question, Answer

# Diğer modelleri düz kayıt edelim
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Answer)

# Question için özel bir admin paneli yapalım
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # Soru listesinde bu sütunlar görünsün
    list_display = ('title', 'author', 'offering', 'current_handler', 'created_at')
    # Sağ tarafta bu filtrelere göre filtreleme yapabilelim
    list_filter = ('offering', 'current_handler', 'created_at')
    # Arama çubuğu bu alanlarda arama yapsın
    search_fields = ('title', 'content', 'author__username')

    # Düzenleme sayfasında alanları gruplayalım
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author')
        }),
        ('Atamalar', {
            'fields': ('offering', 'current_handler')
        }),
    )