from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView)
from ..models import (Libro, Autore, Genere, SottoGenere, Editore, Collana)
from ..forms import (LibroForm, AutoreForm, GenereForm, SottoGenereForm,
                    EditoreForm, CollanaForm)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Dashboard'
        context['tot_libri'] = Libro.objects.all().count()
        return context


# Libri
class CatalogoView(ListView):
    template_name = 'core/catalogo.html'
    model = Libro

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Catalogo'
        context['sottotitolo'] = '({})'.format(Libro.objects.filter(disponibile=True).count())
        return context

    def get_queryset(self):
        queryset = Libro.objects.filter(disponibile=True)
        return queryset


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
    form_class = AutoreForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = self.object.nome_cognome()
        context['sottotitolo'] = 'Modifica'
        return context

    def get_success_url(self):
        return reverse('elenco_autori')


# Generi e sottogeneri

class ElencoGeneriSottogeneriView(LoginRequiredMixin, TemplateView):
    template_name = 'core/elenco_generi_sottogeneri.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        generi_list =  Genere.objects.all()
        sottogeneri_list =  SottoGenere.objects.all()
        context['generi_list'] = generi_list
        context['sottogeneri_list'] = sottogeneri_list
        context['tot_generi'] = generi_list.count()
        context['tot_sottogeneri'] = sottogeneri_list.count()
        context['titolo'] = 'Elenco generi e sottogeneri'
        return context


class AggiungiGenereView(LoginRequiredMixin, CreateView):
    template_name = 'core/genere_form.html'
    model = Genere
    form_class = GenereForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Aggiungi Genere'
        return context

    def get_success_url(self):
        return reverse('elenco_generi_sottogeneri')


class ModificaGenereView(LoginRequiredMixin, UpdateView):
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


class AggiungiSottoGenereView(LoginRequiredMixin, CreateView):
    template_name = 'core/sottogenere_form.html'
    model = SottoGenere
    form_class = SottoGenereForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Aggiungi Sottogenere'
        return context

    def get_success_url(self):
        return reverse('elenco_generi_sottogeneri')


class ModificaSottoGenereView(LoginRequiredMixin, UpdateView):
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

class ElencoEditoriCollaneView(LoginRequiredMixin, TemplateView):
    template_name = 'core/elenco_editori_collane.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        editori_list =  Editore.objects.all()
        collane_list =  Collana.objects.all()
        context['editori_list'] = editori_list
        context['collane_list'] = collane_list
        context['tot_editori'] = editori_list.count()
        context['tot_collane'] = collane_list.count()
        context['titolo'] = 'Elenco Editori e Collane'
        return context


class AggiungiEditoreView(LoginRequiredMixin, CreateView):
    template_name = 'core/editore_form.html'
    model = Editore
    form_class = EditoreForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Aggiungi Editore'
        return context

    def get_success_url(self):
        return reverse('elenco_editori_collane')


class ModificaEditoreView(LoginRequiredMixin, UpdateView):
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


class AggiungiCollanaView(LoginRequiredMixin, CreateView):
    template_name = 'core/collana_form.html'
    model = Collana
    form_class = CollanaForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Aggiungi Collana'
        return context

    def get_success_url(self):
        return reverse('elenco_editori_collane')


class ModificaCollanaView(LoginRequiredMixin, UpdateView):
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
