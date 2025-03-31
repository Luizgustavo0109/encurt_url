from django import forms
from .models import Url

class FormUrl(forms.ModelForm):
    senha = forms.CharField(required=False, widget=forms.PasswordInput)
    data_expiracao = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = Url
        fields = "__all__"