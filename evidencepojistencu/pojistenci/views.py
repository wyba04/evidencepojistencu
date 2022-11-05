from django.shortcuts import render, redirect, reverse
from django.views import generic
from .models import Pojistenec, Uzivatel
from .forms import PojistenecForm, UzivatelForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


class PojistenecIndex(generic.ListView):

    template_name = 'pojistenci/pojistenci_index.html'
    context_object_name = 'pojistenci'

    def get_queryset(self):
        # řazení od nejmenšího po největší
        return Pojistenec.objects.all().order_by('-prijmeni')


class AktualPojistenec(generic.DetailView):

    model = Pojistenec
    template_name = 'pojistenci/pojistenec_detail.html'


class CreatePojistenec(generic.edit.CreateView):
    form_class = PojistenecForm
    template_name = 'pojistenci/create_pojistenec.html'

    # Metoda pro GET request, zobrazí pouze formulář
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # Metoda pro POST request, zkontroluje formulář; pokud je validní, vytvoří nového pojištěnce; pokud ne, zobrazí formulář s chybovou hláškou
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
        return render(request, self.template_name, {"form": form})


class UzivatelViewRegister(generic.edit.CreateView):
    form_class = UzivatelForm
    model = Uzivatel
    template_name = 'pojistenci/user_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
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
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                return redirect('pojistenci')

        return render(request, self.template_name, {'form': form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.info(request, 'Nemůžeš se odhlásit, pokud nejsi přihlášený.')
    return redirect(reverse('login'))
