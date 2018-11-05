from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView)
from ..models import (RichiestaPrestito, Prestito)


class ElencoPrestitiView(LoginRequiredMixin, ListView):
        template_name = 'core/elenco_prestiti'
        model = Prestito

        def get_context_data(self, *args, **kwargs):
            context = super().get_context_data(*args, **kwargs)
            context['titolo'] = 'Elenco Prestiti'
            context['sottotitolo'] = '({})'.format(Prestito.objects.all().count())
            return context
