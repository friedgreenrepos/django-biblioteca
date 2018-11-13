from django import forms
from .models import (Libro, Autore, Editore, Collana, Genere, SottoGenere,
                     Profilo, Segnalazione, Bookmark, Prestito, Documento,
                     DocumentoAmministratore)


__all__ = ['BootstrapForm']


class BootstrapForm(forms.Form):
    ''' A simple Form to apply bootstrap classes to widgets.
    '''
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            name = field.widget.__class__.__name__.lower()
            if not name.startswith("radio") and not name.startswith("checkbox") and not name == 'fileinput':
                try:
                    classes = field.widget.attrs['class'].split(' ')
                    classes.append('form-control')
                    field.widget.attrs['class'] = ' '.join(set(classes))
                except KeyError:
                    field.widget.attrs['class'] = 'form-control'


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
    sospendi = forms.BooleanField(label='Sospendi profilo')

    class Meta:
        model = Segnalazione
        fields = ['tipo', 'descrizione']


class DocumentoForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['nome', 'descrizione', 'file']


class DocumentoAmministratoreForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = DocumentoAmministratore
        fields = ['nome', 'descrizione', 'file']


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
