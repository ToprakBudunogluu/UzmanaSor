from django import forms
from .models import Question, Answer
from accounts.models import CustomUser

# 'ModelForm', 'model'den otomatik olarak form 'field'ları (alanları)
# oluşturmamızı sağlar.
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question # Bu form, 'Question' modelini baz alıyor

        # Kullanıcıdan SADECE bu 'field'ları iste:
        fields = ('title', 'content', 'offering')

class ForwardForm(forms.Form):
    # ModelChoiceField: Veritabanındaki objelerden bir 'dropdown' oluşturur
    recipient = forms.ModelChoiceField(
        # queryset: Bu 'dropdown'ın seçenekleri NELER OLSUN?
        # CustomUser tablosundaki user_type'ı 'teacher' olan HERKES.
        queryset=CustomUser.objects.filter(user_type='teacher'),
        label="Yönlendirilecek Hoca"
    )