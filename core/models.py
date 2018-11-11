from datetime import timedelta
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MaxValueValidator
from .settings import DURATA_PRESTITO, MAX_LIBRI_INPRESTITO, GIORNI_SOSPENSIONE


class TrackProfilo(models.Model):
    tot_libri = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(MAX_LIBRI_INPRESTITO)])
    prestito_sospeso = models.BooleanField(default=False)
    segnalazioni = models.ManyToManyField('Segnalazione', blank=True)
    data_inizio_sospensione = models.DateField(null=True, blank=True)
    data_fine_sospensione = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True

    def calculate_fine_sospensione(self):
        if self.data_inizio_sospensione:
            return self.data_inizio_sospensione + timedelta(GIORNI_SOSPENSIONE)


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

    def __str__(self):
        return '{} {}'.format(self.nome, self.cognome)


class Segnalazione(models.Model):
    DANNEGGIAMENTO = 'D'
    RITARDO = 'R'
    ALTRO = 'A'
    TIPI_MOTIVO = (
        (DANNEGGIAMENTO, 'Danneggiamento'),
        (RITARDO, 'Ritardo consegna'),
        (ALTRO, 'Altro'),
    )
    tipo = models.CharField(max_length=10, choices=TIPI_MOTIVO)
    data = models.DateField(auto_now_add=True)
    descrizione = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Segnalazioni'

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
            return self.prestito_set.all().latest()
        else:
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
    data_richiesta = models.DateField(auto_now_add=True)
    data_prestito = models.DateField(blank=True, null=True)
    data_restituzione = models.DateField(blank=True, null=True)
    profilo = models.ForeignKey(Profilo, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.libro, self.profilo)

    def is_incorso(self):
        return self.stato == self.INCORSO

    def is_richiesto(self):
        return self.stato == self.RICHIESTO

    def calc_data_restituzione(self):
        if self.data_prestito:
            return self.data_prestito + timedelta(days=DURATA_PRESTITO)
        else:
            return None

    def is_prestito_scaduto(self, oggi):
        if self.data_restituzione:
            return oggi > self.data_restituzione
        else:
            return False

    class Meta:
        verbose_name_plural = 'Prestiti'
        unique_together = ('profilo', 'libro')
        get_latest_by = ('-data_richiesta')


class Genere(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Generi'

    def __str__(self):
        return self.nome


class SottoGenere(models.Model):
    nome = models.CharField(max_length=100)
    padre = models.ForeignKey(Genere, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Sottogeneri'

    def __str__(self):
        return self.nome


class Editore(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Editori'

    def __str__(self):
        return self.nome


class Collana(models.Model):
    nome = models.CharField(max_length=100)
    editore = models.ForeignKey(Editore, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Collane'

    def __str__(self):
        return self.nome


class Autore(models.Model):
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Autori'

    def __str__(self):
        return '{} {}'.format(self.nome, self.cognome)

    def nome_cognome(self):
        return '{} {}'.format(self.nome, self.cognome)


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=20)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.nome
