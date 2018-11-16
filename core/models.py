from datetime import timedelta, date
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from .settings import (GIORNI_PRESTITO, MAX_LIBRI_INPRESTITO, GIORNI_SOSPENSIONE,
                      MAXKB_DOCUMENTO)


def valida_documento(documento):
    file_size = documento.file.size
    limit_kb = MAXKB_DOCUMENTO
    if file_size > limit_kb*1024:
        raise ValidationError("La dimensione massima del documento è: {}".format(limit_kb))


class TrackProfilo(models.Model):
    tot_libri = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(MAX_LIBRI_INPRESTITO)])
    tot_richieste = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(MAX_LIBRI_INPRESTITO)])
    segnalazioni = models.ManyToManyField('Segnalazione', blank=True)
    data_inizio_sospensione = models.DateField(null=True, blank=True)
    data_fine_sospensione = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def is_sospeso(self):
        return self.data_fine_sospensione and self.data_fine_sospensione > date.today()

    def calculate_fine_sospensione(self):
        if self.data_inizio_sospensione:
            return self.data_inizio_sospensione + timedelta(GIORNI_SOSPENSIONE)
        else:
            return None


class Profilo(TrackProfilo):
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    codfisc = models.CharField(max_length=16, verbose_name=_('Codice fiscale'))
    data_nascita = models.DateField(verbose_name=_('Data di nascita'))
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        verbose_name_plural = 'Profili'
        unique_together = ("nome", "cognome", "codfisc")
        permissions = (
            ('sospendi_profilo', 'Sospensione dei prestiti per profilo'),
        )
        ordering = ['nome', 'cognome']

    def __str__(self):
        return '{} {}'.format(self.nome, self.cognome)


class Segnalazione(models.Model):
    DANNEGGIAMENTO = 'DAN'
    RITARDO = 'RIT'
    ALTRO = 'ALTRO'
    TIPI_MOTIVO = (
        (DANNEGGIAMENTO, 'Danneggiamento'),
        (RITARDO, 'Ritardo consegna'),
        (ALTRO, 'Altro'),
    )
    tipo = models.CharField(max_length=10, choices=TIPI_MOTIVO)
    descrizione = models.TextField(blank=True)
    data = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Segnalazioni'
        ordering = ['data']

    def __str__(self):
        return self.tipo


class Libro(models.Model):
    isbn = models.CharField(max_length=13, unique=True, verbose_name='ISBN')
    titolo = models.CharField(max_length=100)
    autori = models.ManyToManyField('Autore')
    descrizione = models.TextField(blank=True)
    editore = models.ForeignKey('Editore', on_delete=models.PROTECT)
    genere = models.ForeignKey('Genere', on_delete=models.PROTECT)
    sottogeneri = models.ManyToManyField('SottoGenere', blank=True)
    collana = models.ForeignKey('Collana', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Libri'
        ordering = ['titolo']
        permissions = (
            ('view_dettaglio_libro', 'Accesso al dettaglio di un libro'),
            ('gestisci_prestito', 'Gestione richieste e prestiti'),
        )

    def __str__(self):
        return self.titolo

    def get_absolute_url(self):
        return reverse('dettaglio_libro', kwargs={'pk: self.pk'})

    def get_autori_display(self):
        return ', '.join(autore.nome_cognome() for autore in self.autori.all())
    get_autori_display.short_description = 'Autori'

    def get_titolo_autori_display(self):
        return '{} - {}'.format(self, self.get_autori_display())

    def get_sottogeneri_display(self):
        return ', '.join(sottogenere.nome for sottogenere in self.sottogeneri.all())
    get_sottogeneri_display.short_description = 'Sottogeneri'

    def has_prestiti(self):
        return self.prestito_set.all().exists()

    def is_disponibile(self):
        if not self.has_prestiti():
            return True
        for p in self.prestito_set.all():
            if not p.stato == p.CONCLUSO:
                return False
        return True

    def get_current_prestito(self):
        if self.has_prestiti():
            ultimo = self.prestito_set.all().latest()
            if not ultimo.is_concluso():
                return ultimo
        return None


class Prestito(models.Model):
    RICHIESTO = 'RC'
    INCORSO = 'IC'
    CONCLUSO = 'CN'
    STATI_PRESTITO = (
        (RICHIESTO, 'Richiesto'),
        (INCORSO, 'In corso'),
        (CONCLUSO, 'Concluso'),
    )
    stato = models.CharField(max_length=2, choices=STATI_PRESTITO)
    data_richiesta = models.DateTimeField(auto_now_add=True)
    data_inizio = models.DateField(blank=True, null=True)
    data_scadenza = models.DateField(blank=True, null=True)
    profilo = models.ForeignKey(Profilo, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.libro, self.profilo)

    @property
    def is_scaduto(self):
        if self.data_scadenza:
            return  date.today() >= self.data_scadenza
        else:
            return False

    def is_incorso(self):
        return self.stato == self.INCORSO

    def is_richiesto(self):
        return self.stato == self.RICHIESTO

    def is_concluso(self):
        return self.stato == self.CONCLUSO

    def calc_data_scadenza(self):
        if self.data_inizio:
            return self.data_inizio + timedelta(days=GIORNI_PRESTITO)
        else:
            return None

    class Meta:
        verbose_name_plural = 'Prestiti'
        unique_together = ('profilo', 'libro')
        ordering = ('data_richiesta',)
        get_latest_by = ('data_richiesta',)


class Documento(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descrizione = models.TextField(blank=True)
    file = models.FileField(upload_to='documenti/%Y/%m/',
                            validators=[valida_documento],
                            help_text="Dimensione massima: {} Kb".format(MAXKB_DOCUMENTO))
    data_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Documenti'
        permissions = (
            ('view_dettaglio_documento', 'Accesso al dettaglio del documento'),
        )
        ordering = ['nome']

    def __str__(self):
        return '"{}" - {}'.format(self.nome, self.data_upload.date())


class DocumentoAmministratore(Documento):

    class Meta:
        verbose_name_plural = 'Documenti Amministratore'


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=20)
    urlname = models.CharField(max_length=100)
    args = models.CharField(max_length=100, blank=True, null=True)
    kwargs = models.CharField(max_length=100, blank=True, null=True)
    urlparams = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_bookmark_url(self):
        return "{}?{}".format(reverse(self.urlname, args=self.args, kwargs=self.kwargs), self.urlparams)


class Genere(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Generi'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class SottoGenere(models.Model):
    nome = models.CharField(max_length=100)
    padre = models.ForeignKey(Genere, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Sottogeneri'
        ordering = ['padre']

    def __str__(self):
        return self.nome


class Editore(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Editori'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Collana(models.Model):
    nome = models.CharField(max_length=100)
    editore = models.ForeignKey(Editore, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Collane'
        ordering = ['editore']

    def __str__(self):
        return self.nome


class Autore(models.Model):
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Autori'
        ordering=['nome']

    def __str__(self):
        return '{} {}'.format(self.nome, self.cognome)

    def nome_cognome(self):
        return '{} {}'.format(self.nome, self.cognome)
