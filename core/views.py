from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView)
from .models import Libro

# Create your views here.

class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Dashboard'
        context['tot_libri'] = Libro.objects.all().count()
        return context


class ElencoLibriView(ListView):
    template_name = 'core/elenco_libri.html'
    model = Libro

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Elenco Libri'
        context['sottotitolo'] = Libro.objects.all().count()
        return context


class DettaglioLibroView(DetailView):
    template_name = 'core/dettaglio_libro.html'
    model = Libro
    context_object_name = 'libro'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = self.object
        context['sottotitolo'] = self.object.get_autori_display()
        return context
