from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import (PermissionRequiredMixin,
                                        LoginRequiredMixin, UserPassesTestMixin)
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  FormView)
from ..models import Documento, DocumentoAmministratore
from ..forms import DocumentoForm, DocumentoAmministratoreForm


class ElencoDocumentiView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'core.view_documento'
    template_name = 'core/elenco_documenti.html'
    model = Documento

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = 'Elenco Documenti'
        context['sottotitolo'] = '({})'.format(self.get_queryset().count())
        context['documenti_amministratore'] = DocumentoAmministratore.objects.all()
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


# Documenti Amministratore
class DettaglioDocumentoAmministratoreView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    template_name = 'core/dettaglio_documento.html'
    model = DocumentoAmministratore
    context_object_name = 'documento'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = '{}'.format(self.object)
        context['is_doc_amm'] = True
        return context


class AggiungiDocumentoAmministratoreView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    template_name = 'core/documento_form.html'
    model = DocumentoAmministratore
    form_class = DocumentoAmministratoreForm

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = "Aggiungi Documento Amministratore"
        context['annulla_link'] = reverse('elenco_documenti')
        return context

    def get_success_url(self):
        return reverse('elenco_documenti')

    def form_valid(self, form):
        doc = form.save(commit=False)
        doc.user = self.request.user
        doc.save()
        return HttpResponseRedirect(self.get_success_url())


class ModificaDocumentoAmministratoreView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'core/documento_form.html'
    model = DocumentoAmministratore
    form_class = DocumentoAmministratoreForm

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titolo'] = self.object
        context['sottotitolo'] = 'Modifica'
        context['annulla_link'] = reverse('dettaglio_documento_amministratore', kwargs={'pk': self.object.pk})
        return context

    def get_success_url(self):
        return reverse('elenco_documenti')
