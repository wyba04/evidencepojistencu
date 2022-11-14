from django.shortcuts import render, redirect, reverse
from django.views import generic
from .models import *
from .forms import *
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

    model = SeznamPojisteni
    template_name = 'pojistenci/pojistenec_detail.html'


    def get(self, request, pk):
        
        try:
            pojistenec = Pojistenec.objects.get(id=pk)
        except:
            return redirect('home')
        pojistky = SeznamPojisteni.objects.filter(pojistenec_id=pk)
        context = {'pojistenec':pojistenec,'pojistky':pojistky}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if request.user.is_authenticated:
            if 'edit' in request.POST:
                return redirect('edit_pojistenec', pk=pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, 'Nemáš práva pro smazání pojištěnce.')
                    return redirect(reverse('home'))
                else:
                    Pojistenec(id=pk).delete()
        else:
            pass
        return redirect(reverse('home'))


class CreatePojistenec(generic.edit.CreateView):
    form_class = PojistenecForm
    template_name = 'pojistenci/create_pojistenec.html'

    # Metoda pro GET request, zobrazí pouze formulář
    def get(self, request):
        if not request.user.is_admin:
            messages.info(request, 'Nemáš práva přidat nového pojištěnce.')
            return redirect(reverse('home'))
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # Metoda pro POST request, zkontroluje formulář; pokud je validní, vytvoří nového pojištěnce; pokud ne, zobrazí formulář s chybovou hláškou
    def post(self, request):
        if not request.user.is_admin:
            messages.info(request, 'Nemáš práva přidat nového pojištěnce.')
            return redirect(reverse('home'))
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('home')
        return render(request, self.template_name, {"form": form})


class UzivatelViewRegister(generic.edit.CreateView):
    form_class = UzivatelForm
    model = Uzivatel
    template_name = 'pojistenci/register_form.html'

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'Už jsi přihlášený, nemůžeš se registrovat.')
            return redirect(reverse('home'))
        else:
            form = self.form_class(None)
        # dict(nazev=self.nazev_stranky),
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(
                request, 'Už jsi přihlášený, nemůžeš se registrovat.')
            return redirect(reverse('home'))
        form = self.form_class(request.POST)
        if form.is_valid():
            uzivatel = form.save(commit=False)
            password = form.cleaned_data['password']
            uzivatel.set_password(password)
            uzivatel.save()
            login(request, uzivatel)
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class UzivatelViewLogin(generic.edit.CreateView):
    form_class = LoginForm
    template_name = 'pojistenci/user_form.html'

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'Už jsi přihlášený.')
            return redirect(reverse('home'))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'Už jsi přihlášený.')
            return redirect(reverse('home'))
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
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
            return redirect(reverse('home'))
        try:
            pojistenec = Pojistenec.objects.get(pk=pk)
            
        except:
            messages.error(request, 'Tento pojištěnec neexistuje.')
            return redirect('home')
        form = self.form_class(instance=pojistenec)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, 'Nemáš práva pro úpravu pojištěnce.')
            return redirect(reverse('home'))
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
                return redirect(reverse('home'))
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


class AktualPojistenec(generic.DetailView):

    model = SeznamPojisteni
    template_name = 'pojistenci/pojistenec_detail.html'
    


    def get(self, request, pk):
        
        try:
            pojistenec = Pojistenec.objects.get(id=pk)
        except:
            return redirect('home')
        pojistky = SeznamPojisteni.objects.filter(pojistenec_id=pk)
        total_pojisteni = pojistky.count()
        context = {'pojistenec':pojistenec,'pojistky':pojistky, 'pocet_pojistek':total_pojisteni}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if request.user.is_authenticated:
            if 'edit' in request.POST:
                return redirect('edit_pojistenec', pk=pk)
            else:
                if not request.user.is_admin:
                    messages.info(
                        request, 'Nemáš práva pro smazání pojištěnce.')
                    return redirect('pojistenec_detail', pk=pk)
                else:
                    self.get_object().delete()
                    messages.info(request, 'Pojištěnec byl smazán včetně jeho zaevidovaných pojištění.')
        else:
            messages.info(request, 'Pojištěnec byl smazán včetně jeho zaevidovaných pojištění.')
        return redirect(reverse('home'))
    
    
    
class CreatePojisteni(generic.edit.CreateView):
    form_class = PojisteniForm
    template_name = 'pojistenci/create_pojisteni.html'

    # Metoda pro GET request, zobrazí pouze formulář
    def get(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, 'Nemáš práva přidat nové pojištění.')
            return redirect(reverse('pojistenec_detail', pk=pk))
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # Metoda pro POST request, zkontroluje formulář; pokud je validní, vytvoří nového pojištěnce; pokud ne, zobrazí formulář s chybovou hláškou
    def post(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, 'Nemáš práva přidat nové pojištění.')
            return redirect(reverse('pojistenec_detail', pk=pk))
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('pojistenec_detail', pk=pk)
        return render(request, self.template_name, {"form": form})
    
    
class UpdatePojisteni(LoginRequiredMixin, generic.edit.CreateView):
        form_class = PojisteniForm
        template_name = 'pojistenci/update_pojisteni.html'
        
        
        def get(self, request, pk):
            
            if not request.user.is_admin:
                messages.info(request, 'Nemáš práva na úpravu pojištění.')
                return redirect('home')
            try:
                
                pojisteni = SeznamPojisteni.objects.get(pk=pk)
            except:
                messages.error(request, 'Tento pojištěnec neexistuje.')
                return redirect('pojistenec_detail', pk=pojisteni.id)
            form = self.form_class(instance=pojisteni)
            return render(request, self.template_name, {'form': form})
        
        def post(self, request, pk):
            if not request.user.is_admin:
                messages.info(request, 'Nemáš práva pro úpravu pojištění.')
                return redirect(reverse('pojistenec_detail', pk=pojistenec.id))
            form = self.form_class(request.POST)

            if form.is_valid():
                pojistenec = form.cleaned_data['pojistenec']
                typ_pojisteni = form.cleaned_data['typ_pojisteni']
                predmet_pojisteni = form.cleaned_data['predmet_pojisteni']
                hodnota_pojisteni = form.cleaned_data['hodnota_pojisteni']
                plati_od = form.cleaned_data['plati_od']
                plati_do = form.cleaned_data['plati_do']
                poznamka = form.cleaned_data['poznamka']
                try:
                    pojisteni = SeznamPojisteni.objects.get(pk=pk)
                except:
                    messages.error(request, 'Tento pojištěnec neexistuje.')
                    return redirect(reverse('home'))
                pojisteni.pojistenec = pojistenec
                pojisteni.typ_pojisteni = typ_pojisteni
                pojisteni.predmet_pojisteni = predmet_pojisteni
                pojisteni.hodnota_pojisteni = hodnota_pojisteni
                pojisteni.plati_od = plati_od
                pojisteni.plati_do = plati_do
                pojisteni.poznamka = poznamka
                pojisteni.save()
            return redirect('pojistenec_detail', pk=pojistenec.id)

        
def delete_pojisteni(request, pk):
    pojisteni = SeznamPojisteni.objects.get(pk=pk)
    pojistenec = pojisteni.pojistenec.id
    
    
    if request.method == "POST":
        pojistenec = SeznamPojisteni.objects.get(id=pk)
        pojisteni.delete()
        return redirect('pojistenec_detail', pk=pojistenec.id)
    
    context = {'pojisteni':pojisteni, 'pojistenec':pojistenec}
    return render(request, 'pojistenci/delete_pojisteni.html', context)

