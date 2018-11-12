from datetime import date
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  FormView)
from ..models import (Libro, Profilo, Prestito)
from ..forms import (ProfiloForm, PrestitoForm, SegnalazioneLibroForm,
                     ProfiloSelectForm)
from .mixins import FilteredQuerysetMixin
from .filters import PrestitoFilter


class ElencoPrestitiView(PermissionRequiredMixin, LoginRequiredMixin, FilteredQuerysetMixin, ListView):
    permission_required = 'core.view_prestito'
    template_name = 'core/elenco_prestiti.html'
    model = Prestito
    filter_class = PrestitoFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Elenco Prestiti'
        context['sottotitolo'] = '({})'.format(self.get_queryset().count())
        return context


class DettaglioPrestitoView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'core.view_dettaglio_prestito'
    template_name = 'core/dettaglio_prestito.html'
    model = Prestito
    context_object_name = 'prestito'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = '"{}"'.format(self.object.libro.get_titolo_autori_display())
        context['sottotitolo'] = '({})'.format(self.object.get_stato_display())
        return context


class PrestitoUpdateProfiloView(CreateView):
    template_name = 'core/prestito_update_profilo.html'
    model = Prestito
    form_class = PrestitoForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        libro = Libro.objects.get(pk=self.kwargs['libro_pk'])
        context['libro'] = libro
        context['titolo'] = 'Richiesta Prestito: "{}"'.format(libro.get_titolo_autori_display())
        return context

    def get_success_url(self):
        return reverse('catalogo')

    def form_valid(self, form):
        prestito = form.instance
        try:
            with transaction.atomic():
                libro = Libro.objects.get(pk=self.kwargs['libro_pk'])
                prestito.libro = libro
                prestito.stato = Prestito.RICHIESTO
                prestito.save()
                messages.success(self.request, "Richiesta prestito registrata con successo!")

        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return HttpResponseRedirect(self.get_success_url())


class PrestitoCreateProfiloView(FormView):
    template_name = 'core/prestito_create_profilo.html'
    form_class = ProfiloForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        libro = Libro.objects.filter(pk=self.kwargs['libro_pk']).first()
        context['titolo'] = 'Richiesta Prestito: "{}"'.format(libro.get_titolo_autori_display())
        return context

    def get_success_url(self):
        return reverse('catalogo')

    def form_valid(self, form):
        profilo = form.save()

        try:
            with transaction.atomic():
                libro = Libro.objects.get(pk=self.kwargs['libro_pk'])
                prestito_dict = {
                    'libro': libro,
                    'profilo': profilo,
                    'stato': Prestito.RICHIESTO
                }
                prestito = Prestito.objects.create(**prestito_dict)
                prestito.save()
                messages.success(self.request, "Richiesta prestito registrata con successo!")

        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return HttpResponseRedirect(self.get_success_url())


class ConsegnaLibroPrestitoView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'core.gestisci_prestito'
    model = Prestito

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                prestito = Prestito.objects.select_for_update(nowait=True).get(pk=self.kwargs['pk'])
                if prestito.is_incorso():
                    messages.error(self.request, "Questo prestito è già in corso.")
                    return HttpResponseRedirect(redirect_to=reverse('dettaglio_prestito', kwargs={'pk': prestito.pk}))
                prestito.stato = Prestito.INCORSO
                prestito.profilo.tot_libri += 1
                prestito.data_prestito = date.today()
                prestito.save()
                prestito.data_restituzione = prestito.calc_data_restituzione()
                prestito.save()
                messages.success(self.request, "Consegna libro registrata con successo.")
        except ObjectDoesNotExist:
            messages.error(self.request)
        return HttpResponseRedirect(redirect_to=reverse('dettaglio_prestito', kwargs={'pk': prestito.pk}))


class RifiutaRichiestaPrestitoView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'core.gestisci_prestito'
    model = Prestito

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                prestito = Prestito.objects.select_for_update(nowait=True).get(pk=self.kwargs['pk'])
                prestito.delete()
                messages.success(self.request, "Richiesta prestito rifiutata.")

        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return HttpResponseRedirect(redirect_to=reverse('elenco_prestiti'))


class RestituzioneLibroPrestitoView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'core.gestisci_prestito'
    model = Prestito

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                prestito = Prestito.objects.select_for_update(nowait=True).get(pk=self.kwargs['pk'])
                if prestito.is_richiesto():
                    messages.error(self.request, "Questo prestito non è ancora stato consegnato.")
                    return HttpResponseRedirect(redirect_to=reverse('dettaglio_prestito', kwargs={'pk': prestito.pk}))

                prestito.stato = Prestito.CONCLUSO
                prestito.profilo.tot_libri -= 1
                prestito.save()
                messages.success(self.request, "Restituzione libro registrata con successo!")

        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return HttpResponseRedirect(redirect_to=reverse('elenco_prestiti'))


class SospendiPrestitoProfiloView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'core.gestisci_prestito'
    template_name = 'core/prestito_sospensione_form.html'
    model = Libro
    form_class = SegnalazioneLibroForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        profilo = Profilo.objects.filter(pk=self.kwargs['profilo_pk']).first()
        context['titolo'] = 'Sospensione Prestito: "{}"'.format(profilo)
        return context

    def get_success_url(self):
        return reverse('elenco_prestiti')

    def form_valid(self, form):
        segnalazione = form.save()
        try:
            with transaction.atomic():
                profilo = Profilo.objects.select_for_update(nowait=True).get(pk=self.kwargs['profilo_pk'])
                profilo.prestito_sospeso = True
                profilo.segnalazioni_set = segnalazione
                profilo.data_inizio_sospensione = date.today()
                profilo.save()
                profilo.data_fine_sospensione = profilo.calculate_fine_sospensione()
                profilo.save()
                messages.success(self.request, "Segnalazione effettuata con successo.")
        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return HttpResponseRedirect(self.get_success_url())
