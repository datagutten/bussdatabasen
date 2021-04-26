from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

import bussdatabase.utils as utils
from .Buss import Buss


class Bilde(models.Model):
    buss = models.ForeignKey(Buss, on_delete=models.PROTECT, related_name='images')
    bilde = models.ImageField(upload_to='bussbilder/')
    synlig = models.BooleanField(default=True)
    toppbilde = models.BooleanField(default=False)
    bildetekst = models.CharField(max_length=100, blank=True, null=True)
    fotograf = models.CharField(max_length=100, blank=True, null=True)
    lagt_til = models.DateTimeField(auto_now_add=True)
    lagt_til_av = models.ForeignKey('auth.User',
                                    on_delete=models.PROTECT,
                                    related_name='images',
                                    null=True)
    endret = models.DateTimeField(auto_now=True)
    endret_av = models.ForeignKey('auth.User',
                                  on_delete=models.PROTECT,
                                  related_name='image_changed',
                                  null=True)

    class Meta:
        verbose_name_plural = 'bilder'

    def __str__(self):
        return str(self.bilde)

    def bussnavn(self):
        return self.buss.navn()

    def kan_endre(self, user):
        return utils.can_edit(self.lagt_til_av, user, 'bussdatabase.change_bilde')


# Receive the post_delete signal
# and delete the file associated with the model instance.
# https://stackoverflow.com/a/14310174/2630074

@receiver(post_delete, sender=Bilde)
def bilde_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.bilde.delete(False)
