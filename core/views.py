from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView)
from .models import Libro

# Create your views here.

class ElencoLibriView(PermissionRequiredMixin, ListView):
    permission_required = 'core.view_libro'
    template_name = 'core/elenco_libri.html'
    model = Libro


class DashboardView:
    template_name = 'dashboard.html'
