from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, ForwardForm, AnswerForm
from .models import QuestionBinderTest, Answer


def home(request):
    # Bu fonksiyon şimdilik sadece bir HTML sayfasını 'render' edecek
    # (yani kullanıcıya gösterecek).

    # 'core/home.html' dosyasını ara ve kullanıcıya gönder
    return render(request, 'core/home.html')


@login_required 
def student_dashboard(request):

    if request.user.user_type not in ('student', 'r_student'):
        # O zaman bu sayfayı görme izni YOKTUR. Anasayfaya yolla.
        return redirect('core:home')

    # 1. KENDİ SORULARINI LİSTELEMEK İÇİN SORGULA
    # 'author'u (soran) 'request.user' (giriş yapan öğrenci)
    # olan tüm soruları bul. En yeniler üste gelsin.
    # my_questions = QuestionBinderTest.objects.filter(
    #     author=request.user
    # ).order_by('-created_at')

    my_questions_test = QuestionBinderTest.objects.filter(
        question_author = request.user
    )
    # .order_by('-question.created_at')

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # 1. 'ModelForm'dan gelen 'title' ve 'content' ile objeyi yarat
            question = form.save(commit=False) 

            # 2. 'author'u manuel ata
            question.question_author = request.user 
            question.question_current_handler = question.course.course_teacher
            question.question_priority = 1
            # question.question.title = form.cleaned_data.get('title_data')
            # question.question.content = form.cleaned_data.get('content_data')
            # if assigned_teacher:
            #     # Eğer öğrenci bir hoca seçtiyse...
            #     question.current_handler = assigned_teacher
            # else:
            #     # Seçmediyse 'current_handler' 'None' (boş) kalır
            #     # ve soru 'havuza' düşer.

            #     # 4. Kaydet (Bu, 'Question.save()' metodunu tetikler)
            question.save() 

            return redirect('core:student_dashboard')

    # 3. YENİ SORU FORMUNU GÖSTER (Bu kısım aynı)
    else:
        form = QuestionForm() 

    # 4. 'CONTEXT'İ GÜNCELLE
    # 'template'e artık HEM formu HEM DE soru listesini yolla
    context = {
        'form': form,
        'my_questions': my_questions_test
    }
    return render(request, 'core/dashboard_student.html', context)

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
    my_questions = QuestionBinderTest.objects.filter(
        question_current_handler_id = request.user.id
    )
    # .order_by('-priority', '-created_at')
    


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
    question = get_object_or_404(QuestionBinderTest, pk=pk)

    if not (request.user.user_type == 'teacher' or request.user == question.question_author):
        # O zaman bu sayfayı görme izni YOKTUR. Anasayfaya yolla.
        return redirect('core:home')

    # Bu soruya daha önce yazılmış CEVAPLARI al
    answers = question.answers.all().order_by('-created_at')

    # İki formu da 'None' olarak başlat
    forward_form = None
    answer_form = None

    # Logic: Sadece 'teacher'lar cevaplayabilir ve 'forward' edebilir
    if request.user.user_type == 'teacher':

        # --- POST İSTEĞİNİ İŞLEME (Kullanıcı Butona Bastıysa) ---
        if request.method == 'POST':

            # Hangi butona basıldığını ayırt etmemiz lazım.
            # 'name' attribute'ü ile yapacağız.

            # EĞER "FORWARD ET" BUTONUNA BASILDIYSA:
            if 'forward_submit' in request.POST:
                forward_form = ForwardForm(request.POST)
                if forward_form.is_valid():
                    new_handler = forward_form.cleaned_data['recipient']

                    question.question_old_handler = question.question_current_handler 
                    question.question_current_handler = new_handler          
                    question.save() 

                    return redirect('core:teacher_dashboard')

            # EĞER "CEVAPLA" BUTONUNA BASILDIYSA:
            elif 'answer_submit' in request.POST:
                answer_form = AnswerForm(request.POST)
                if answer_form.is_valid():
                    # commit=False: Henüz kaydetme
                    answer = answer_form.save(commit=False) 

                    # Cevabın 'author' (yazarı) ve 'question' (sorusu)
                    # alanlarını manuel ata
                    answer.author = request.user
                    answer.question = question
                    answer.save() # Şimdi kaydet

                    # Başarılı, aynı sayfaya yönlendir (cevap görünsün)
                    return redirect('core:question_detail', pk=question.pk)

        # --- GET İSTEĞİNİ İŞLEME (Sayfa İlk Açıldıysa) ---
        # İki formun da boş halini oluştur
        forward_form = ForwardForm()
        answer_form = AnswerForm()

    # --- TÜM VERİYİ TEMPLATE'E YOLLA ---
    context = {
        'question': question,
        'answers': answers, # Cevap listesini de yolla
        'forward_form': forward_form,
        'answer_form': answer_form,
    }
    return render(request, 'core/question_detail.html', context)