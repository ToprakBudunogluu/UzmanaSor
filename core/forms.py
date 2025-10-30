from django import forms
from .models import  Answer, QuestionBinderTest
from accounts.models import CustomUser

# 'ModelForm', 'model'den otomatik olarak form 'field'ları (alanları)
# oluşturmamızı sağlar.
class QuestionForm(forms.ModelForm):

    # # YENİ ALAN: Hocaya direkt atama
    # # Bu, 'Question' modelinde olmayan 'sanal' bir alan.
    # handler_assignment = forms.ModelChoiceField(
    #     queryset=CustomUser.objects.filter(user_type='teacher'),
    #     required=False, # 'False' yap ki, 'havuza' (None) atabilsinler
    #     label="Direkt Hocaya Ata (Opsiyonel)",
    #     # 'widget'ını da Bootstrap'e uyumlu hale getirelim
    #     widget=forms.Select(attrs={'class': 'form-select'})
    # )



    class Meta:
        
        model = QuestionBinderTest
        # 'fields' listesinden 'offering'i (dersliği) ÇIKARDIK.
        fields = ('title', 'content' , 'course' , 'class_term') # Sadece bu ikisini 'model'den al
        
    # '__init__' ile formun kalanını da güzelleştirelim
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['course'].widget.attrs['class'] = 'form-select'
        self.fields['class_term'].widget.attrs['class'] = 'form-select'

   


class ForwardForm(forms.Form):
    # ModelChoiceField: Veritabanındaki objelerden bir 'dropdown' oluşturur
    recipient = forms.ModelChoiceField(
        # queryset: Bu 'dropdown'ın seçenekleri NELER OLSUN?
        # CustomUser tablosundaki user_type'ı 'teacher' olan HERKES.
        queryset=CustomUser.objects.filter(user_type='teacher'),
        label="Yönlendirilecek Hoca",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        # Kullanıcıdan SADECE 'content' (içerik) alanını iste
        fields = ('content',)
        labels = {
            'content': 'Cevabınız'
        }

    # Formu 'Bootstrap' ile güzelleştirelim (Ders 12.5'ten)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cevap 'textarea'sına 'form-control' class'ı ekle
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['rows'] = 5 # 5 satır yüksekliğinde