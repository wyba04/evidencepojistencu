from dataclasses import fields
from django.forms import *
from .models import *


class PojistenecForm(forms.ModelForm):
    """
    Formulář pro zadání pojištěnce
    """
    class Meta:
        model = Pojistenec
       # stat = forms.ModelChoiceField(queryset=Stat.objects.all())
        fields = ['jmeno', 'prijmeni', 'email',
                  'telefon', 'ulice_cp', 'mesto', 'psc', 'stat']


class UzivatelForm(forms.ModelForm):
    """
    Registrační formulář
    """
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Uzivatel
        fields = ['email', 'password']


class LoginForm(forms.Form):
    """
    Login formulář
    """
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['email', 'password']
        

class PojisteniForm(forms.ModelForm):
    """
    Formulář pro zadání pojištění
    """
    class Meta:
        model = SeznamPojisteni
        fields = ['pojistenec', 'typ_pojisteni', 'predmet_pojisteni', 'hodnota_pojisteni', 'plati_od', 'plati_do', 'poznamka']


class PojistnaUdalostForm(forms.ModelForm):
    """ 
    Formulář pro zadání pojistné události
    """
    class Meta:
        model = PojistneUdalosti
        fields = ['pojisteni', 'datum_udalosti', 'cas_udalosti', 'popis_skody', 'vycisleni_skody']
