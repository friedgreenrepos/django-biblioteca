from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import (PermissionRequiredMixin,
                                        LoginRequiredMixin, UserPassesTestMixin)
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  FormView)
from ..models import Documento
from ..forms import DocumentoForm
from .mixins import FilteredQuerysetMixin
from .filters import DocumentoFilter


class ElencoDocumentiView(PermissionRequiredMixin, LoginRequiredMixin, FilteredQuerysetMixin, ListView):
    permission_required = 'core.view_documento'
    template_name = 'core/elenco_documenti.html'
    model = Documento
    filter_class = DocumentoFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Elenco Documenti'
        context['sottotitolo'] = '({})'.format(self.get_queryset().count())
        # FilteredQuerysetMixin overridden
        filters = self.get_filter_obj()
        if filters is not None:
            kwargs['object_list'] = filters.qs
            if not self.request.user.is_staff:
                context['object_list'] = filters.qs.filter(is_amministrazione=False)
            kwargs['filter'] = filters
        return context

# Documenti
class DettaglioDocumentoView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'core.view_dettaglio_documento'
    template_name = 'core/dettaglio_documento.html'
    model = Documento
    context_object_name = 'documento'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = '{}'.format(self.object)
        return context


class AggiungiDocumentoView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'core.add_documento'
    template_name = 'core/documento_form.html'
    model = Documento
    form_class = DocumentoForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = "Aggiungi Documento"
        context['annulla_link'] = reverse('elenco_documenti')
        return context

    def get_success_url(self):
        return reverse('elenco_documenti')

    def form_valid(self, form):
        doc = form.save(commit=False)
        doc.user = self.request.user
        doc.save()
        return HttpResponseRedirect(self.get_success_url())


class ModificaDocumentoView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'core.change_documento'
    template_name = 'core/documento_form.html'
    model = Documento
    form_class = DocumentoForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = self.object
        context['sottotitolo'] = 'Modifica'
        context['annulla_link'] = reverse('dettaglio_documento', kwargs={'pk': self.object.pk})
        return context

    def get_success_url(self):
        return reverse('elenco_documenti')
