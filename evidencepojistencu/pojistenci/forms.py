from dataclasses import fields
from django import forms
from django import forms
from .models import *


class PojistenecForm(forms.ModelForm):

    class Meta:
        model = Pojistenec
       # stat = forms.ModelChoiceField(queryset=Stat.objects.all())
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
        

class PojisteniForm(forms.ModelForm):
    class Meta:
        model = SeznamPojisteni
        fields = ['pojistenec', 'typ_pojisteni', 'predmet_pojisteni', 'hodnota_pojisteni', 'plati_od', 'plati_do', 'poznamka']
