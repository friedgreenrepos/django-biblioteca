from django import forms
from .utils import BootstrapForm
from .models import (Libro, Autore, Editore, Collana, Genere, SottoGenere,
                     Profilo, Segnalazione, Bookmark, Prestito, Documento)
from .settings import GIORNI_SOSPENSIONE


class PrestitoForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Prestito
        fields = ['profilo']


class LibroForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['isbn', 'titolo', 'autori', 'descrizione', 'editore',
                  'genere', 'sottogeneri', 'collana']


class ProfiloForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Profilo
        fields = ['nome', 'cognome', 'codfisc', 'data_nascita', 'telefono',
                  'email']


class SegnalazioneForm(BootstrapForm, forms.ModelForm):
    sospendi = forms.BooleanField(label='Sospendi profilo',
                                  help_text='(Il profilo rimarrà sospeso per {} giorni)'.format(GIORNI_SOSPENSIONE),
                                  required=False,
                                  initial=True)

    class Meta:
        model = Segnalazione
        fields = ['tipo', 'descrizione']


class DocumentoForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['nome', 'descrizione', 'file', 'is_amministrazione']


class BookmarkForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ['nome', 'urlname', 'urlparams']
        widgets = {
            'urlname': forms.HiddenInput(),
            'urlparams': forms.HiddenInput(),
        }


class AutoreForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Autore
        fields = ['nome', 'cognome']


class EditoreForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Editore
        fields = ['nome']


class CollanaForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Collana
        fields = ['nome', 'editore']


class GenereForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Genere
        fields = ['nome']


class SottoGenereForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = SottoGenere
        fields = ['nome', 'padre']
