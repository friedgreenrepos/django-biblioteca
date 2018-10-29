from django.db import models

# Create your models here.


class Genere(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class InfoLibro(models.Model):
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    titolo = models.CharField(max_length=100)
    autori = models.ManyToManyField('Autore')
    descrizione = models.TextField(blank=True)
    editore = models.CharField(max_length=100)
    genere = models.ManyToManyField('Genere')


    class Meta:
        ordering = ('titolo',)

    def __str__(self):
        return self.titolo


class TrackLibro(models.Model):
    pass


class Autore(models.Model):
    pass
