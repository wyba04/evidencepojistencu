from dataclasses import fields
from django import forms
from django import forms
from .models import Pojistenec, Uzivatel


class PojistenecForm(forms.ModelForm):

    class Meta:
        model = Pojistenec
        fields = ['jmeno', 'prijmeni', 'email',
                  'telefon', 'ulice_cp', 'mesto', 'psc', 'stat']
        
class UzivatelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Uzivatel
        fields = ['email', 'password']
        
        
class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        fields = ['email', 'password']
