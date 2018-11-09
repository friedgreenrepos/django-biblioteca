from datetime import date
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView)
from ..models import (Libro, Profilo)
from ..forms import (ProfiloForm, ProfiloLibroForm, LibroPrestitoForm)
from .mixins import FilteredQuerysetMixin


class ElencoPrestitiView(PermissionRequiredMixin, ListView):
    permission_required = 'core.view_prestito'
    template_name = 'core/elenco_prestiti.html'
    model = Libro

    def get_queryset(self):
        qs = Libro.objects.filter(Q(stato_prestito=Libro.INPRESTITO) | Q(stato_prestito=Libro.PENDENTE))
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Elenco Prestiti'
        context['sottotitolo'] = '({})'.format(self.get_queryset().count())
        return context


class DettaglioPrestitoView(PermissionRequiredMixin, DetailView):
    permission_required = 'core.view_dettaglio_prestito'
    template_name = 'core/dettaglio_prestito.html'
    model = Libro
    context_object_name = 'libro'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = '"{}"'.format(self.object.get_titolo_autori_display())
        context['sottotitolo'] = '({})'.format(self.object.get_stato_prestito_display())
        return context


class PrestitoCreateProfiloView(CreateView):
    template_name = 'core/prestito_create_profilo.html'
    model = Libro
    form_class = ProfiloLibroForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        libro = Libro.objects.get(pk=self.kwargs['pk'])
        context['titolo'] = 'Richiesta Prestito: "{}"'.format(libro.get_titolo_autori_display())
        return context

    def get_success_url(self):
        return reverse('catalogo')

    def form_valid(self, form):
        profilo_prestito = form.save()
        try:
            with transaction.atomic():
                libro = Libro.objects.select_for_update(nowait=True).get(pk=self.kwargs['pk'])
                if libro.is_inprestito():
                    messages.error(self.request, "Questo prestito è già in corso")
                    return HttpResponseRedirect(redirect_to=reverse('catalogo'))
                if libro.is_pendente():
                    messages.error(self.request, "Questo prestito è già stato richiesto")
                    return HttpResponseRedirect(redirect_to=reverse('catalogo'))
                libro.profilo_prestito = profilo_prestito
                libro.stato_prestito = Libro.PENDENTE
                libro.data_richiesta = date.today()
                libro.save()
                messages.success(self.request, "Richiesta prestito registrata con successo!")
        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return HttpResponseRedirect(self.get_success_url())


class PrestitoUpdateProfiloView(UpdateView):
    template_name = 'core/prestito_update_profilo.html'
    model = Libro
    form_class = LibroPrestitoForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        libro = Libro.objects.get(pk=self.kwargs['pk'])
        context['titolo'] = 'Richiesta Prestito: "{}"'.format(libro.get_titolo_autori_display())
        return context

    def get_success_url(self):
        return reverse('catalogo')

    def form_valid(self, form):
        self.object = form.save()
        try:
            with transaction.atomic():
                libro = Libro.objects.select_for_update(nowait=True).get(pk=self.kwargs['pk'])
                if libro.is_inprestito():
                    messages.error(self.request, "Questo prestito è già in corso")
                    return HttpResponseRedirect(redirect_to=reverse('catalogo'))
                if libro.is_pendente():
                    messages.error(self.request, "Questo prestito è già stato richiesto")
                    return HttpResponseRedirect(redirect_to=reverse('catalogo'))

                libro.stato_prestito = Libro.PENDENTE
                libro.data_richiesta = date.today()
                libro.save()
                messages.success(self.request, "Richiesta prestito registrata con successo!")
        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return HttpResponseRedirect(self.get_success_url())


class ConsegnaLibroPrestitoView(PermissionRequiredMixin, DetailView):
    permission_required = 'core.gestisci_prestito'
    model = Libro

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                libro = Libro.objects.select_for_update(nowait=True).get(pk=self.kwargs['pk'])
                if libro.is_inprestito():
                    messages.error(self.request, "Questo prestito è già in corso")
                    return HttpResponseRedirect(redirect_to=reverse('dettaglio_prestito', kwargs={'pk':libro.pk}))
                if libro.is_disponibile():
                    messages.error(self.request, "Nessun utente ha richiesto questo prestito")
                    return HttpResponseRedirect(redirect_to=reverse('elenco_prestiti'))

                libro.profilo_prestito.tot_libri += 1
                libro.stato_prestito = Libro.INPRESTITO
                libro.data_richiesta = None
                libro.data_prestito = date.today()
                libro.save()
                libro.data_restituzione = libro.calculate_data_restituzione()
                libro.save()
                messages.success(self.request, "Consegna libro registrata con successo!")

        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return HttpResponseRedirect(redirect_to=reverse('dettaglio_prestito', kwargs={'pk':libro.pk}))


class RifiutaRichiestaPrestitoView(PermissionRequiredMixin, DetailView):
    permission_required = 'core.gestisci_prestito'
    model = Libro

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            with transaction.atomic():
                libro = Libro.objects.select_for_update(nowait=True).get(pk=self.kwargs['pk'])
                if libro.is_inprestito():
                    messages.error(self.request, "Questo prestito è già in corso")
                    return HttpResponseRedirect(redirect_to=reverse('dettaglio_prestito', kwargs={'pk':libro.pk}))
                if libro.is_disponibile():
                    messages.error(self.request, "Nessun utente ha richiesto questo prestito")
                    return HttpResponseRedirect(redirect_to=reverse('elenco_prestiti'))

                libro.stato_prestito = Libro.DISPONIBILE
                libro.profilo_prestito = None
                libro.data_richiesta = None
                libro.save()
                messages.success(self.request, "Richiesta prestito rifiutata.")

        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return HttpResponseRedirect(redirect_to=reverse('elenco_prestiti'))


class RestituzioneLibroPrestitoView(PermissionRequiredMixin, DetailView):
    permission_required = 'core.gestisci_prestito'
    model = Libro

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            with transaction.atomic():
                libro = Libro.objects.select_for_update(nowait=True).get(pk=self.kwargs['pk'])
                if libro.is_pendente():
                    messages.error(self.request, "Questo prestito non è ancora stato consegnato.")
                    return HttpResponseRedirect(redirect_to=reverse('dettaglio_prestito', kwargs={'pk':libro.pk}))
                if libro.is_disponibile():
                    messages.error(self.request, "Nessun utente ha richiesto questo prestito.")
                    return HttpResponseRedirect(redirect_to=reverse('elenco_prestiti'))

                libro.stato_prestito = Libro.DISPONIBILE
                libro.data_richiesta = None
                libro.data_prestito = None
                libro.data_restituzione = None
                libro.profilo_prestito.tot_libri -= 1
                libro.profilo_prestito = None
                libro.save()
                messages.success(self.request, "Restituzione libro registrata con successo!")

        except ObjectDoesNotExist as err:
            messages.error(self.request, err)
        return HttpResponseRedirect(redirect_to=reverse('elenco_prestiti'))


    class SospendiPrestitoView(PermissionRequiredMixin,):
        permission_required = 'core.gestisci_prestito'
