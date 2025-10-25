from django.urls import path
from . import views # <-- 'Bu klasördeki views.py dosyasını import et'

# URL'leri app bazında ayırmak için (İyi bir alışkanlıktır)
app_name = 'core' 

urlpatterns = [
    path('', views.home, name='home'), # Ana sayfa için URL deseni

    path('dashboard/', views.student_dashboard, name='student_dashboard'),

    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # <int:pk>: "Buraya bir 'integer' (sayı) gelecek,
    # ve bu sayıyı 'view' fonksiyonuna 'pk' (primary key) 
    # adında bir 'variable' (değişken) olarak yolla."
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
]