from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class StudentRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Formda sadece bu alanları göster:
        fields = ('username', 'email')

        def __init__(self, *args, **kwargs):
            # Önce 'parent' (ebeveyn) class'ın (UserCreationForm)
            # '__init__' metodunu çalıştır ki, form normal şekilde kurulsun
            super().__init__(*args, **kwargs)

            # Artık formun 'fields' (alanları) oluşturuldu.
            # Bir 'loop' (döngü) ile tüm 'fields'ları (username, email,
            # password1, password2) gezelim:
            for fieldname in self.fields:
                # O 'field'ın 'widget'ını (görselini, yani <input> tag'ini)
                # 'attrs' (nitelikler) sözlüğünü bul...
                # ve o sözlüğe 'class' anahtarıyla 'form-control' değerini ekle.
                self.fields[fieldname].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        # Formdan gelen 'user' objesini al
        user = super().save(commit=False) 

        # --- BURASI ÇOK ÖNEMLİ ---
        # user_type'ı 'student' olarak MANUEL ayarla.
        # Böylece bu formu dolduran herkes OTOMATİK olarak öğrenci olur.
        user.user_type = 'student'

        # Eğer 'commit' True ise (ki varsayılanı 'True'dur),
        # kullanıcıyı veritabanına kaydet.
        if commit:
            user.save()
        return user