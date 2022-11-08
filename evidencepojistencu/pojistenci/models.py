
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class TypPojisteni(models.Model):
    nazev_pojisteni = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'Typ pojištění: {self.nazev_pojisteni}'

    class Meta:
        verbose_name = 'Typ pojištění'
        verbose_name_plural = 'Typy pojištění'


class Stat(models.Model):
    stat = models.CharField(max_length=50)

    ordering = ['-stat']

    def __str__(self) -> str:
        return self.stat

    class Meta:
        verbose_name = 'Stát'
        verbose_name_plural = 'Státy'


class Pojistenec(models.Model):
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
        return f'Jméno: {self.jmeno}, Příjmení: {self.prijmeni} | Email: {self.email} | Ulice: {self.ulice_cp}, Město: {self.mesto}'

    class Meta:
        verbose_name = 'Pojištěnec'
        verbose_name_plural = 'Pojištěnci'


class SeznamPojisteni(models.Model):
    pojistenec = models.ForeignKey(
        Pojistenec, on_delete=models.SET_NULL, null=True)
    typ_pojisteni = models.ForeignKey(
        TypPojisteni, on_delete=models.SET_NULL, null=True)
    predmet_pojisteni = models.CharField(max_length=80)
    hodnota_pojisteni = models.CharField(max_length=10)
    plati_od = models.CharField(max_length=10)
    plati_do = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f'Pojištěnec: {self.pojistenec.jmeno} {self.pojistenec.prijmeni} | Pojištění: {self.typ_pojisteni.nazev_pojisteni} | Částka: {self.hodnota_pojisteni}'

    class Meta:
        verbose_name = 'Seznam pojištění'
        verbose_name_plural = 'Seznam pojištění'


class UzivatelManager(BaseUserManager):
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
        verbose_name = 'uživatel'
        verbose_name_plural = 'uživatelé'

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
