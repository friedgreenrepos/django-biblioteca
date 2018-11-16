import logging

from django.db.models import Q
from dal import autocomplete
from ..models import Autore, Editore, Collana, Genere, Profilo

logger = logging.getLogger(__name__)

class AutoreDalView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Autore.objects.all()

        if self.q:
            qs = qs.filter(Q(nome__istartswith=self.q) | Q(cognome__istartswith=self.q))

        return qs


class EditoreDalView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Editore.objects.all()

        if self.q:
            qs = qs.filter(nome__istartswith=self.q)

        return qs


class CollanaDalView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Collana.objects.all()

        editore_id = self.forwarded.get('editore', None)

        if editore_id:
            logger.debug("editore id: {}".format(editore_id))
            qs = qs.filter(editore_id=editore_id)

        if self.q:
            qs = qs.filter(nome__istartswith=self.q)

        return qs


class GenereDalView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Genere.objects.all()

        if self.q:
            qs = qs.filter(nome__istartswith=self.q)

        return qs
