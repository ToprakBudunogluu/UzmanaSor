from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, ForwardForm
from .models import Question

def home(request):
    # Bu fonksiyon şimdilik sadece bir HTML sayfasını 'render' edecek
    # (yani kullanıcıya gösterecek).

    # 'core/home.html' dosyasını ara ve kullanıcıya gönder
    return render(request, 'core/home.html')


@login_required
def student_dashboard(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # commit=False: 
            # "ObjeYİ OLUŞTUR AMA VERİTABANINA HENÜZ KAYDETME!"
            # Çünkü 'author' (soran) alanını eklememiz lazım.
            question = form.save(commit=False)

            # 'author'u, o an giriş yapmış olan kullanıcı olarak ata
            question.author = request.user 

            # Şimdi veritabanına kaydet.
            # BU NOKTADA bizim 'Question.save()' metodumuz
            # çalışıp 'priority' ve 'handler'ı da atayacak.
            question.save() 

            # Başarılı. Anasayfaya yönlendir.
            return redirect('core:home')

    # Eğer kullanıcı sayfayı İLK KEZ AÇIYORSA (GET):
    else:
        form = QuestionForm() # Boş bir form oluştur

    # Formu (boş veya hatalı) 'template'e yolla
    return render(request, 'core/dashboard_student.html', {'form': form})


@login_required # 1. Fedai: Önce giriş yapmış olmalı
def teacher_dashboard(request):
    # 2. Fedai: Sadece 'teacher' tipindekiler girebilir
    if request.user.user_type != 'teacher':
        # Eğer 'student' veya 'r_student' buraya girmeye çalışırsa,
        # anasayfaya geri yolla.
        return redirect('core:home')

    # 3. Veritabanı Sorgusu (THE QUERY):
    # 'Question' modelinde, 'current_handler' alanı
    # 'request.user' (yani o an giriş yapmış olan hoca) olan
    # TÜM soruları bul.
    #
    # 'order_by': Onları 'priority' (önem) sırasına göre Z->A (-priority)
    # ve 'created_at' (tarih) sırasına göre en yeni (-created_at)
    # olacak şekilde sırala.
    my_questions = Question.objects.filter(
        current_handler_id = request.user.id
    ).order_by('-priority', '-created_at')
    


    # 4. Veriyi 'Context'e Koy:
    # Bulduğumuz soru listesini 'template'e yollamak için bir 'dictionary' hazırla
    context = {
        'questions': my_questions
    }

    # 5. Render:
    # 'context'i al ve 'dashboard_teacher.html' template'ine yolla
    return render(request, 'core/dashboard_teacher.html', context)


@login_required
def question_detail(request, pk):
    # 1. 'pk' ile soruyu bul.
    question = get_object_or_404(Question, pk=pk)

    # 2. Formu işle (Eğer kullanıcı "Forward" butonuna bastıysa - POST)
    if request.method == 'POST':
        # TODO: Burası 'Answer' (Cevap) formuyla çakışabilir.
        # Şimdilik sadece 'Forward' olduğunu varsayalım.
        form = ForwardForm(request.POST)
        if form.is_valid():
            new_handler = form.cleaned_data['recipient']

            # --- BASİT YOL LOGIC'İ ---
            question.old_handler = question.current_handler # Eskiyi 'old'a kaydır
            question.current_handler = new_handler          # Yeniyi 'current'a ata
            question.save() # Güncelle
            # --- LOGIC BİTTİ ---

            return redirect('core:teacher_dashboard')

    # 3. Formu göster (Eğer kullanıcı sayfayı ilk açtıysa - GET)
    else:
        form = ForwardForm()

    # 4. Veriyi 'template'e yolla
    context = {
        'question': question,
        'forward_form': form,
        # 'history' (tarihçe) diye bir şey yollamıyoruz artık
    }
    return render(request, 'core/question_detail.html', context)