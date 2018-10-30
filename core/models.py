from django.db import models

# Create your models here.


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


class Autore(models.Model):
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Autori'

    def __str__(self):
        return '{} {}'.format(self.cognome, self.nome)

    def cognome_nome(self):
        return '{} {}'.format(self.cognome, self.nome)


class TrackLibro(models.Model):
    disponibile = models.BooleanField(default=True)
    data_restituzione = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True


class Libro(TrackLibro):
    isbn = models.CharField(max_length=13, unique=True, verbose_name='ISBN')
    titolo = models.CharField(max_length=100)
    autori = models.ManyToManyField('Autore')
    descrizione = models.TextField(blank=True)
    editore = models.ForeignKey(Editore, on_delete=models.PROTECT)
    genere = models.ForeignKey(Genere, on_delete=models.PROTECT)
    sottogenere = models.ManyToManyField(SottoGenere, blank=True)
    collana = models.CharField(max_length=100)


    class Meta:
        verbose_name_plural = 'Libri'
        ordering = ['titolo']

    def __str__(self):
        return self.titolo

    def get_autori_display(self):
        return ', '.join(autore.cognome_nome() for autore in self.autori.all())
    get_autori_display.short_description = 'Autori'
