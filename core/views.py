from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView)
from .models import Libro
from .forms import LibroForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Dashboard'
        context['tot_libri'] = Libro.objects.all().count()
        return context


class ElencoLibriView(LoginRequiredMixin, ListView):
    template_name = 'core/elenco_libri.html'
    model = Libro

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Elenco Libri'
        context['sottotitolo'] = Libro.objects.all().count()
        return context


class DettaglioLibroView(LoginRequiredMixin, DetailView):
    template_name = 'core/dettaglio_libro.html'
    model = Libro
    context_object_name = 'libro'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = self.object
        context['sottotitolo'] = self.object.get_autori_display()
        return context


class AggiungiLibroView(LoginRequiredMixin, CreateView):
    template_name = 'core/libro_form.html'
    model = Libro
    context_object_name = 'libro'
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
    fields = ['__all__']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = '{} - {}'.format(self.object, self.get_autori_display())
        context['sottotitolo'] = 'Modifica'
        return context

    def get_success_url(self):
        return reverse('dettaglio_libro', kwargs={'pk': self.object.pk})
