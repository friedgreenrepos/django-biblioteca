from datetime import date
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, FormView)
from ..models import (Libro, Autore, Genere, SottoGenere, Editore, Collana,
                      Bookmark, Prestito)
from ..forms import (LibroForm, AutoreForm, GenereForm, SottoGenereForm,
                     EditoreForm, CollanaForm, BookmarkForm)
from .filters import LibroFilter
from .mixins import FilteredQuerysetMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Dashboard'
        context['tot_libri'] = Libro.objects.all().count()
        return context


class CatalogoView(FilteredQuerysetMixin, ListView):
    template_name = 'core/catalogo.html'
    model = Libro
    filter_class = LibroFilter

    def get_queryset(self):
        qs = Libro.objects.all()
        for lib in qs:
            if not lib.is_disponibile():
                qs = qs.exclude(pk=lib.pk)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Catalogo'
        return context


class ElencoLibriView(PermissionRequiredMixin, FilteredQuerysetMixin, LoginRequiredMixin, ListView):
    permission_required = 'core.view_libro'
    template_name = 'core/elenco_libri.html'
    model = Libro
    filter_class = LibroFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Elenco Libri'
        context['bookmark_form'] = BookmarkModelForm(initial={ 'url': self.request.get_full_path()})
        return context


class DettaglioLibroView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'core.view_dettaglio_libro'
    template_name = 'core/dettaglio_libro.html'
    model = Libro
    context_object_name = 'libro'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = '"{}"'.format(self.object.get_titolo_autori_display())
        context['current_prestito'] = self.object.get_current_prestito()
        return context


class AggiungiLibroView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'core.add_libro'
    template_name = 'core/libro_form.html'
    model = Libro
    form_class = LibroForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Aggiungi Libro'
        return context

    def get_success_url(self):
        return reverse('elenco_libri')


class ModificaLibroView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'core.change_autore'
    template_name = 'core/libro_form.html'
    model = Libro
    form_class = LibroForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = self.object.get_titolo_autori_display()
        context['sottotitolo'] = 'Modifica'
        return context

    def get_success_url(self):
        return reverse('dettaglio_libro', kwargs={'pk': self.object.pk})


class AggiungiBookmarkView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'core.add_bookmark'
    model = Bookmark
    form_class = BookmarkForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

    def get_success_url(self):
        return reverse('elenco_libri')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Autori
class ElencoAutoriView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'core.view_autore'
    template_name = 'core/elenco_autori.html'
    model = Autore

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Elenco Autori'
        context['sottotitolo'] = '({})'.format(Autore.objects.all().count())
        return context


class AggiungiAutoreView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'core.add_autore'
    template_name = 'core/autore_form.html'
    model = Autore
    form_class = AutoreForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Aggiungi Autore'
        return context

    def get_success_url(self):
        return reverse('elenco_autori')


class ModificaAutoreView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'core.change_autore'
    template_name = 'core/autore_form.html'
    model = Autore
    form_class = AutoreForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = self.object.nome_cognome()
        context['sottotitolo'] = 'Modifica'
        return context

    def get_success_url(self):
        return reverse('elenco_autori')


# Generi e sottogeneri
class ElencoGeneriSottogeneriView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    permission_required = 'core.view_genere'
    template_name = 'core/elenco_generi_sottogeneri.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        generi_list = Genere.objects.all()
        sottogeneri_list = SottoGenere.objects.all()
        context['generi_list'] = generi_list
        context['sottogeneri_list'] = sottogeneri_list
        context['tot_generi'] = generi_list.count()
        context['tot_sottogeneri'] = sottogeneri_list.count()
        context['titolo'] = 'Elenco generi e sottogeneri'
        return context


class AggiungiGenereView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'core.add_genere'
    template_name = 'core/genere_form.html'
    model = Genere
    form_class = GenereForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Aggiungi Genere'
        return context

    def get_success_url(self):
        return reverse('elenco_generi_sottogeneri')


class ModificaGenereView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'core.change_genere'
    template_name = 'core/genere_form.html'
    model = Genere
    form_class = GenereForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = self.object
        context['sottotitolo'] = 'Modifica'
        return context

    def get_success_url(self):
        return reverse('elenco_generi_sottogeneri')


class AggiungiSottoGenereView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'core.add_sottogenere'
    template_name = 'core/sottogenere_form.html'
    model = SottoGenere
    form_class = SottoGenereForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Aggiungi Sottogenere'
        return context

    def get_success_url(self):
        return reverse('elenco_generi_sottogeneri')


class ModificaSottoGenereView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'core.change_sottogenere'
    template_name = 'core/sottogenere_form.html'
    model = SottoGenere
    form_class = SottoGenere

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = self.object
        context['sottotitolo'] = 'Modifica'
        return context

    def get_success_url(self):
        return reverse('elenco_generi_sottogeneri')


# Editori e collane
class ElencoEditoriCollaneView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    permission_required = 'core.view_editore'
    template_name = 'core/elenco_editori_collane.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        editori_list = Editore.objects.all()
        collane_list = Collana.objects.all()
        context['editori_list'] = editori_list
        context['collane_list'] = collane_list
        context['tot_editori'] = editori_list.count()
        context['tot_collane'] = collane_list.count()
        context['titolo'] = 'Elenco Editori e Collane'
        return context


class AggiungiEditoreView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'core.add_editore'
    template_name = 'core/editore_form.html'
    model = Editore
    form_class = EditoreForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Aggiungi Editore'
        return context

    def get_success_url(self):
        return reverse('elenco_editori_collane')


class ModificaEditoreView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'core.change_editore'
    template_name = 'core/editore_form.html'
    model = Editore
    form_class = EditoreForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = self.object
        context['sottotitolo'] = 'Modifica'
        return context

    def get_success_url(self):
        return reverse('elenco_editori_collane')


class AggiungiCollanaView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'core.add_collana'
    template_name = 'core/collana_form.html'
    model = Collana
    form_class = CollanaForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Aggiungi Collana'
        return context

    def get_success_url(self):
        return reverse('elenco_editori_collane')


class ModificaCollanaView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'core.change_collana'
    template_name = 'core/collana_form.html'
    model = Collana
    form_class = CollanaForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = self.object
        context['sottotitolo'] = 'Modifica'
        return context

    def get_success_url(self):
        return reverse('elenco_editori_collane')
