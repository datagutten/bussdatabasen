from django.db import models
from .models import Selskap, Karosserifabrikk, Chassisprodusent, Tilstand
from .models import Status

# from .Bilde import Bilde


class Buss(models.Model):
    TILSTAND_CHOICES = (
        (1, 'Helrestaurert'),
        (2, 'Oppusset'),
        (3, 'Urestaurert'),
        (4, 'Under restaurering'),
        (5, 'Hensatt'),
        (6, 'Ombygget'),
        (7, 'Avskiltet'),
        (8, 'Hogget'),
        (9, 'Solgt til utlandet'),
        (None, 'Ikke oppgitt'),
    )

    selskap = models.ForeignKey(Selskap, on_delete=models.PROTECT, null=True, blank=True)
    internnummer = models.CharField(max_length=10, blank=True, null=True)
    registreringsnummer = models.CharField(max_length=8,
                                           blank=True,
                                           null=True,
                                           unique=True)
    understellsnummer = models.CharField(max_length=50,
                                         blank=True,
                                         null=True)
    opprinnelig_registreringsnummer = models.CharField(max_length=8,
                                                       blank=True,
                                                       null=True)
    karosserifabrikk = models.ForeignKey(Karosserifabrikk,
                                         on_delete=models.PROTECT, blank=True, null=True)
    karosseritype = models.CharField(max_length=200, blank=True, null=True)
    byggnummer = models.CharField(max_length=200, blank=True, null=True,
                                  help_text='Karosseriets byggnummer')
    chassisprodusent = models.ForeignKey(Chassisprodusent,
                                         on_delete=models.PROTECT, blank=True, null=True)
    chassistype = models.CharField(max_length=200, blank=True, null=True)
    motor = models.CharField(max_length=200, blank=True, null=True)
    ytelse = models.CharField(max_length=200,
                              blank=True,
                              null=True,
                              help_text='Ytelse i Hk')
    eier = models.CharField(max_length=200, blank=True, null=True)
    byggeår = models.DecimalField(max_digits=4,
                                  decimal_places=0,
                                  blank=True,
                                  null=True)

    lengde = models.DecimalField(max_digits=4,
                                 decimal_places=2,
                                 blank=True,
                                 null=True,
                                 help_text='Bussens lengde i meter')

    bredde = models.DecimalField(max_digits=4,
                                 decimal_places=2,
                                 blank=True,
                                 null=True,
                                 help_text='Bussens bredde i meter')

    vekt = models.IntegerField(blank=True, null=True,
                               help_text='Bussens egenvekt i kg')
    akselavstand = models.DecimalField(max_digits=4,
                                       decimal_places=2,
                                       blank=True,
                                       null=True)
    sitteplasser =\
        models.DecimalField(max_digits=3,
                            decimal_places=0,
                            blank=True,
                            null=True)
    ståplasser =\
        models.DecimalField(max_digits=3,
                            decimal_places=0,
                            blank=True,
                            null=True)
    tilstand =\
        models.ForeignKey(Tilstand,
                          on_delete=models.PROTECT, blank=True, null=True)
    status =\
        models.ForeignKey(Status,
                          on_delete=models.PROTECT, blank=True, null=True)
    tittel =\
        models.CharField(max_length=100, blank=True, null=True,
                         help_text='Kort tittel eller slagord for busen')
    beskrivelse =\
        models.TextField(blank=True, null=True,
                         help_text='Fortell om bussen og dens historie')
    merknad =\
        models.TextField(blank=True, null=True,
                         help_text='Hvis det mangler korrekt valgmulighet \
                         for noe kan informasjonen oppgis her')
    lagt_til = models.DateTimeField(auto_now_add=True)
    lagt_til_av =\
        models.ForeignKey('auth.User',
                          on_delete=models.PROTECT, related_name='Lagt_til_av')
    endret = models.DateTimeField(auto_now=True)
    endret_av = models.ForeignKey('auth.User',
                                  on_delete=models.PROTECT,
                                  related_name='Endret_av')

    class Meta:
        verbose_name_plural = 'busser'
        ordering = ['byggeår']

    def navn(self):
        navn = ''
        if self.selskap:
            navn += self.selskap.navn + ' '
        if self.internnummer:
            if self.selskap and self.selskap.forkortelse:
                navn = self.selskap.forkortelse + ' ' + self.internnummer
            else:
                navn += self.internnummer
        elif self.registreringsnummer:
            navn += self.registreringsnummer
        else:
            navn = 'Buss id %d' % self.pk
        return navn

    def navn_kort(self):
        navn = ''
        if not self.internnummer:
            return
        if self.selskap and self.selskap.forkortelse:
            navn += self.selskap.forkortelse + ' '
        navn += self.internnummer
        return navn

    def chassis(self):
        chassis = ''
        if self.chassisprodusent:
            chassis += '%s ' % self.chassisprodusent
        if self.chassistype:
            chassis += self.chassistype
        return chassis

    def __str__(self):
        return self.navn()

    def toppbilde(self):
        from .Bilde import Bilde
        bilde = Bilde.objects.filter(buss=self, toppbilde=1)
        if bilde:
            return bilde[0]

    def bilder(self):
        from .Bilde import Bilde
        bilder = Bilde.objects.filter(buss=self, toppbilde=0)
        if bilder:
            return bilder

    def kan_endre(self, user):
        if user == self.lagt_til_av:
            return True
        elif user.has_perm('bussdatabase.change_buss'):
            return True
        else:
            return False

    def vekt_tonn(self):
        if self.vekt:
            return self.vekt/1000
        else:
            return None
