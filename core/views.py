from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView)
from .models import (Libro, Autore, Genere, SottoGenere, Editore, Collana)
from .forms import (LibroForm, AutoreForm, GenereForm, SottoGenereForm,
                    EditoreForm, CollanaForm)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Dashboard'
        context['tot_libri'] = Libro.objects.all().count()
        return context

# Libri
class ElencoLibriView(LoginRequiredMixin, ListView):
    template_name = 'core/elenco_libri.html'
    model = Libro

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Elenco Libri'
        context['sottotitolo'] = '({})'.format(Libro.objects.all().count())
        return context


class DettaglioLibroView(LoginRequiredMixin, DetailView):
    template_name = 'core/dettaglio_libro.html'
    model = Libro
    context_object_name = 'libro'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = self.object.get_titolo_autori_display()
        context['sottotitolo'] = 'Dettagli'
        return context


class AggiungiLibroView(LoginRequiredMixin, CreateView):
    template_name = 'core/libro_form.html'
    model = Libro
    form_class = LibroForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Aggiungi Libro'
        return context

    def get_success_url(self):
        return reverse('elenco_libri')


class ModificaLibroView(LoginRequiredMixin, UpdateView):
    template_name = 'core/libro_form.html'
    model = Libro
    context_object_name = 'libro'
    form_class = LibroForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = self.object.get_titolo_autori_display()
        context['sottotitolo'] = 'Modifica'
        return context

    def get_success_url(self):
        return reverse('dettaglio_libro', kwargs={'pk': self.object.pk})


# Autori

class ElencoAutoriView(LoginRequiredMixin, ListView):
    template_name = 'core/elenco_autori.html'
    model = Autore

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Elenco Autori'
        context['sottotitolo'] = '({})'.format(Autore.objects.all().count())
        return context


class AggiungiAutoreView(LoginRequiredMixin, CreateView):
    template_name = 'core/autore_form.html'
    model = Autore
    form_class = AutoreForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Aggiungi Autore'
        return context

    def get_success_url(self):
        return reverse('elenco_autori')


class ModificaAutoreView(LoginRequiredMixin, UpdateView):
    template_name = 'core/autore_form.html'
    model = Autore
    context_object_name = 'autore'
    form_class = AutoreForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = self.object.nome_cognome()
        context['sottotitolo'] = 'Modifica'
        return context

    def get_success_url(self):
        return reverse('elenco_autori')
