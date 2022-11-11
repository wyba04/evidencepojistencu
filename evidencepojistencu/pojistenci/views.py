from django.shortcuts import render, redirect, reverse
from django.views import generic
from .models import *
from .forms import PojistenecForm, UzivatelForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class PojistenecIndex(generic.ListView):

    template_name = 'pojistenci/pojistenci_index.html'
    context_object_name = 'pojistenci'

    def get_queryset(self):
        # řazení od nejmenšího po největší
        return Pojistenec.objects.all().order_by('-prijmeni')


class AktualPojistenec(generic.DetailView):

    model = Pojistenec
    template_name = 'pojistenci/pojistenec_detail.html'

    def get(self, request, pk):
        try:
            pojistenec = self.get_object()
        except:
            return redirect('pojistenci')
        return render(request, self.template_name, {'pojistenec': pojistenec})

    def post(self, request, pk):
        if request.user.is_authenticated:
            if 'edit' in request.POST:
                return redirect('edit_pojistenec', pk=self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, 'Nemáš práva pro smazání pojištěnce.')
                    return redirect(reverse('pojistenci'))
                else:
                    self.get_object().delete()
        else:
            pass
        return redirect(reverse('pojistenci'))


class CreatePojistenec(generic.edit.CreateView):
    form_class = PojistenecForm
    template_name = 'pojistenci/create_pojistenec.html'

    # Metoda pro GET request, zobrazí pouze formulář
    def get(self, request):
        if not request.user.is_admin:
            messages.info(request, 'Nemáš práva přidat nového pojištěnce.')
            return redirect(reverse('pojistenci'))
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # Metoda pro POST request, zkontroluje formulář; pokud je validní, vytvoří nového pojištěnce; pokud ne, zobrazí formulář s chybovou hláškou
    def post(self, request):
        if not request.user.is_admin:
            messages.info(request, 'Nemáš práva přidat nového pojištěnce.')
            return redirect(reverse('pojistenci'))
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('pojistenci')
        return render(request, self.template_name, {"form": form})


class UzivatelViewRegister(generic.edit.CreateView):
    form_class = UzivatelForm
    model = Uzivatel
    template_name = 'pojistenci/register_form.html'

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(
                request, 'Už jsi přihlášený, nemůžeš se registrovat.')
            return redirect(reverse('pojistenci'))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {'form': form})  #dict(nazev=self.nazev_stranky),

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(
                request, 'Už jsi přihlášený, nemůžeš se registrovat.')
            return redirect(reverse('pojistenci'))
        form = self.form_class(request.POST)
        if form.is_valid():
            uzivatel = form.save(commit=False)
            password = form.cleaned_data['password']
            uzivatel.set_password(password)
            uzivatel.save()
            login(request, uzivatel)
            return redirect('pojistenci')
        return render(request, self.template_name, {'form': form})


class UzivatelViewLogin(generic.edit.CreateView):
    form_class = LoginForm
    template_name = 'pojistenci/user_form.html'

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'Už jsi přihlášený.')
            return redirect(reverse('pojistenci'))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'Už jsi přihlášený.')
            return redirect(reverse('pojistenci'))
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('pojistenci')
            else:
                messages.error(request, 'Tento účet neexistuje.')

        return render(request, self.template_name, {'form': form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.info(request, 'Nemůžeš se odhlásit, pokud nejsi přihlášený.')
    return redirect(reverse('login'))


class EditPojistenec(LoginRequiredMixin, generic.edit.CreateView):
    form_class = PojistenecForm
    template_name = 'pojistenci/create_pojistenec.html'

    def get(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, 'Nemáš práva na úpravu pojištěnce.')
            return redirect(reverse('pojistenci'))
        try:
            pojistenec = Pojistenec.objects.get(pk=pk)
        except:
            messages.error(request, 'Tento pojištěnec neexistuje.')
            return redirect('pojistenci')
        form = self.form_class(instance=pojistenec)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, 'Nemáš práva pro úpravu pojištěnce.')
            return redirect(reverse('pojistenci'))
        form = self.form_class(request.POST)

        if form.is_valid():
            jmeno = form.cleaned_data['jmeno']
            prijmeni = form.cleaned_data['prijmeni']
            email = form.cleaned_data['email']
            telefon = form.cleaned_data['telefon']
            ulice_cp = form.cleaned_data['ulice_cp']
            mesto = form.cleaned_data['mesto']
            psc = form.cleaned_data['psc']
            stat = form.cleaned_data['stat']
            try:
                pojistenec = Pojistenec.objects.get(pk=pk)
            except:
                messages.error(request, 'Tento pojištěnec neexistuje.')
                return redirect(reverse('pojistenci'))
            pojistenec.jmeno = jmeno
            pojistenec.prijmeni = prijmeni
            pojistenec.email = email
            pojistenec.telefon = telefon
            pojistenec.ulice_cp = ulice_cp
            pojistenec.mesto = mesto
            pojistenec.psc = psc
            pojistenec.stat = stat
            pojistenec.save()
        return redirect('pojistenec_detail', pk=pojistenec.id)
    
class SeznamPojistek(generic.ListView):

    template_name = 'pojistenci/pojistenec_detail.html'
    context_object_name = 'pojistkyseznam'

    def get_queryset(self):
        # řazení od nejmenšího po největší
        return SeznamPojisteni.objects.all() 
    
    
class TestSeznam(generic.ListView):
    
    template_name = 'pojistenci/testseznam.html'
    context_object_name = 'testsz'
    
    def get_queryset(self):
        return SeznamPojisteni.objects.all()  
    
    

    
    