
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django import forms
# Create your models here.


class TypPojisteni(models.Model):
    """
    Vytvoření tabulky s typy pojištění
    """
    nazev_pojisteni = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nazev_pojisteni

    class Meta:
        verbose_name = 'Druh pojištění'
        verbose_name_plural = 'Druhy pojištění'


class Stat(models.Model):
    """
    Vytvoření tabulky států pro výběr státu ve formuláři
    """
    stat = models.CharField(max_length=50)

    ordering = ['-stat']

    def __str__(self) -> str:
        return self.stat

    class Meta:
        verbose_name = 'Stát'
        verbose_name_plural = 'Státy'


class Pojistenec(models.Model):
    """
    Vytvoření tabulky pojištěnce
    """
    jmeno = models.CharField(max_length=200, verbose_name='Jméno')
    prijmeni = models.CharField(max_length=200, verbose_name='Příjmení')
    email = models.EmailField(max_length=200)
    telefon = models.CharField(max_length=15, verbose_name='Telefon')
    ulice_cp = models.CharField(
        max_length=200, verbose_name='Ulice a číslo popisné')
    mesto = models.CharField(max_length=100, verbose_name='Město')
    psc = models.CharField(max_length=9, verbose_name='PSČ')
    stat = models.ForeignKey(
        Stat, on_delete=models.SET_NULL, null=True, verbose_name='Stát')

    def __init__(self, *args, **kwargs):
        super(Pojistenec, self).__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.jmeno}, {self.prijmeni} | Ulice: {self.ulice_cp}, Město: {self.mesto}'

    class Meta:
        verbose_name = 'Pojištěnec'
        verbose_name_plural = 'Pojištěnci'


class SeznamPojisteni(models.Model):
    """
    Vytvoření tabulky seznamu pojištění
    """
    pojistenec = models.ForeignKey(
        Pojistenec, null=True, on_delete=models.CASCADE, verbose_name='Pojištěnec')
    typ_pojisteni = models.ForeignKey(
        TypPojisteni, null=True, on_delete=models.SET_NULL, verbose_name='Druh pojištění')
    predmet_pojisteni = models.CharField(max_length=80, null=True, verbose_name='Předmět pojištění')
    hodnota_pojisteni = models.CharField(max_length=10, null=True, verbose_name='Hodnota pojištění')
    plati_od = models.CharField(max_length=10, null=True, verbose_name='Platí od')
    plati_do = models.CharField(max_length=10, null=True, verbose_name='Platí do')
    poznamka = models.TextField(null=True, verbose_name='Poznámka', blank=True) # není povinné pole
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Datum vytvoření')

    class Meta:
        verbose_name = 'Seznam pojištění'
        verbose_name_plural = 'Seznam pojištění'

    def __str__(self):
        return f'{self.pojistenec.jmeno} {self.pojistenec.prijmeni} | {self.typ_pojisteni.nazev_pojisteni} | Předmět pojištění: {self.predmet_pojisteni} | Částka: {self.hodnota_pojisteni}'


class PojistneUdalosti(models.Model):
    """
    Vytvoření tabulky pojistných událostí
    """
    pojisteni = models.ForeignKey(SeznamPojisteni, null=True, on_delete=models.CASCADE, verbose_name='Pojištění')
    datum_udalosti = models.CharField(max_length=10, null=True, verbose_name='Datum události')
    cas_udalosti = models.CharField(max_length=10, null=True, verbose_name='Čas události')
    popis_skody = models.TextField(null=True, verbose_name='Popis škodní údálosti')
    vycisleni_skody = models.CharField(max_length=10, null=True, verbose_name='Vyčíslení hodnoty škody')
    
    class Meta:
        verbose_name = 'Pojistná událost'
        verbose_name_plural = 'Pojistné události'
        
    def __str__(self):
        return f'{self.pojisteni.pojistenec.jmeno} {self.pojisteni.pojistenec.prijmeni} | Pojistka č: {self.pojisteni.id}'
    
    


class UzivatelManager(BaseUserManager):
    """
    Změna registrace do admin části na email
    """
    # tvorba uživatele
    def create_user(self, email, password):
        print(self.model)
        if email and password:
            user = self.model(email=self.normalize_email(email))
            user.set_password(password)
            user.save()
        return user

    # tvorba admin uživatele
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save()
        return user


class Uzivatel(AbstractBaseUser):

    email = models.EmailField(max_length=300, unique=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Uživatel'
        verbose_name_plural = 'Uživatelé'

    objects = UzivatelManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'email: {self.email}'

    @property
    def is_staff(self):  # metoda vrací zda je uživatel administrátor
        return self.is_admin

    # metoda zjišťuje, zda má uživatel dané specifické povolení, pro neaktivní uživatele vrací False. My vrátíme vždy True.
    def has_perm(self, perm, obj=None):
        return True

    # vrací True pokud má uživatel nějaká povolení pro daný modul.
    def has_module_perms(self, app_label):
        return True
