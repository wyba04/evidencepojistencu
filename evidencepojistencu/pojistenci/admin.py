from django.contrib import admin
from django import forms
from .models import Pojistenec, SeznamPojisteni, TypPojisteni, UzivatelManager, Uzivatel
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UzivatelCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Uzivatel
        fields = ['email']

    def save(self, commit=False):
        if self.is_valid():
            user = super().save(commit=True)
            user.set_password(self.cleaned_data['password'])
            if commit:
                user.save()
            return user


class UzivatelChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Uzivatel
        fields = ['email', 'is_admin']

    def __init__(self, *args, **kwargs):
        super(UzivatelChangeForm, self).__init__(*args, **kwargs)
        self.Meta.fields.remove('password')


class UzivatelAdmin(UserAdmin):
    form = UzivatelChangeForm
    add_form = UzivatelCreationForm

    list_display = ['email', 'is_admin']
    list_filter = ['is_admin']
    fieldsets = (
        (None, {'fields': ['email', 'password']}),
        ('Permissions', {'fields': ['is_admin']}),
    )

    add_fieldsets = (
        (None, {'fields': ['email', 'password']}
         ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = []


# Register your models here.
admin.site.register(Pojistenec)
admin.site.register(TypPojisteni)
admin.site.register(SeznamPojisteni)
admin.site.register(Uzivatel, UzivatelAdmin)
