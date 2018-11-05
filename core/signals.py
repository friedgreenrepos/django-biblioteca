from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profilo

@receiver(post_save, sender=User)
def crea_profilo_utente(sender, instance, created, **kwargs):
    if created:
        Profilo.objects.create(utente=instance)

@receiver(post_save, sender=User)
def salva_profilo_utente(sender, instance, **kwargs):
    instance.profilo.save()
