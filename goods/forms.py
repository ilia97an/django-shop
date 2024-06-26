from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

class OrderProductForm(forms.Form):
  count = forms.IntegerField(help_text="Введите количество товара")
  
  def clean_count(self):
    data = self.cleaned_data['count']
    
    # Check if count is not too small
    if data < 1:
      raise ValidationError(_('Неправильное количество - заказано ноль'))
    
    # Check if count is not too big
    if data > 100:
      raise ValidationError(_('Неправильное количество - заказано слишком много'))
    
    return data


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    multiple = True

class AddCPUForm(forms.Form):
  name = forms.CharField(help_text="Введите название", required=False)
  price = forms.IntegerField(help_text="Введите цену", required=False)
#  images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple':True}),
  images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple':True}),
                            help_text="Загрузите картинку", required=False)

