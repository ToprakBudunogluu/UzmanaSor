from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import StudentRegistrationForm

def register_student(request):
    # Eğer kullanıcı formu doldurup 'POST' (gönder) tuşuna bastıysa:
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)

        # Formun 'valid' (geçerli) olup olmadığını kontrol et
        # (Şifreler uyuşuyor mu? Username daha önce alınmış mı? vb.)
        if form.is_valid():
            form.save() # Formun kendi .save() metodunu çağır (bizim yazdığımız)

            # Kayıt başarılı, kullanıcıyı anasayfaya yönlendir
            # 'core:home' -> 'core' app'inin 'home' isimli URL'i
            return redirect('core:home')

    # Eğer kullanıcı sayfayı ilk kez yüklüyorsa ('GET' request):
    else:
        form = StudentRegistrationForm() # Boş bir form oluştur

    # 'form'u al ve 'accounts/register.html' template'ine gönder
    return render(request, 'accounts/register.html', {'form': form})