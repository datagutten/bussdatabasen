from django.db import models
import bussdatabase.utils as utils


class Selskap(models.Model):
    navn = models.CharField(max_length=200, unique=True)
    navn2 = models.CharField(max_length=200, unique=True, verbose_name='Alternativt navn', blank=True, null=True)
    forkortelse = models.CharField(max_length=10, blank=True, null=True)
    wikipedia = models.URLField(max_length=200, blank=True, null=True,
                                help_text='Link til wikipediaartikkel om selskapet')
    se_ogsa =\
        models.ManyToManyField('self', blank=True, verbose_name='Se også', db_table='selskap_related', )
    sted = models.CharField(max_length=200, blank=True, null=True)
    lagt_til = models.DateTimeField(auto_now_add=True)
    endret = models.DateTimeField(auto_now=True)
    lagt_til_av =\
        models.ForeignKey('auth.User',
                          on_delete=models.PROTECT,
                          related_name='Selskap_Lagt_til_av')
    endret_av =\
        models.ForeignKey('auth.User',
                          on_delete=models.PROTECT,
                          related_name='Selskap_Endret_av',
                          null=True, blank=True)

    class Meta:
        verbose_name_plural = 'selskaper'
        ordering = ['navn']

    def link(self):
        if self.navn.find('/') == -1:
            return self.navn
        else:
            return self.id

    def kan_endre(self, user):
        return utils.can_edit(self.lagt_til_av, user, 'bussdatabase.change_selskap')

    def wikipedia_navn(self):
        return utils.wikipedia_navn(self.wikipedia)

    def __str__(self):
        return str(self.navn)


class Karosserifabrikk(models.Model):
    navn = models.CharField(max_length=200, unique=True)
    alternativt_navn = models.CharField(max_length=200, blank=True, null=True)
    forkortelse = models.CharField(max_length=200, blank=True, null=True)
    første_år = models.IntegerField(blank=True, null=True)
    siste_år = models.IntegerField(blank=True, null=True)
    antall = models.IntegerField(blank=True, null=True)
    rutebil_nr = models.CharField(max_length=200, blank=True, null=True)
    sted = models.CharField(max_length=200, blank=True, null=True)
    wikipedia = models.URLField(max_length=200, blank=True, null=True)
    se_ogsa = \
        models.ManyToManyField('self', blank=True, verbose_name='Se også')
    lagt_til = models.DateTimeField(auto_now_add=True)
    endret = models.DateTimeField(auto_now=True)
    lagt_til_av =\
        models.ForeignKey('auth.User',
                          on_delete=models.PROTECT,
                          related_name='Karoserrifabrikk_Lagt_til_av')
    endret_av =\
        models.ForeignKey('auth.User',
                          on_delete=models.PROTECT,
                          related_name='Karoserrifabrikk_Endret_av',
                          null=True, blank=True)

    class Meta:
        verbose_name_plural = 'karoserrifabrikker'
        ordering = ['navn']

    def bevarte(self):
        from bussdatabase.models import Buss
        return Buss.objects.filter(karosserifabrikk=self)

    def antall_bevarte(self):
        return self.bevarte().count()

    def link(self):
        return self.forkortelse or self.id

    def wikipedia_navn(self):
        return utils.wikipedia_navn(self.wikipedia)

    # def kan_endre(self, user):
    #    if user == self.lagt_til_av:
    #        return True
    #    elif user.has_perm('bussdatabase.change_karosserifabrikk') or user.is_superuser:
    #        return True
    #    else:
    #        return False

    def kan_endre(self, user):
        return utils.can_edit(self.lagt_til_av, user, 'bussdatabase.change_karosserifabrikk')

    def __str__(self):
        return '%s (%s)' % (str(self.navn), str(self.sted))


class Chassisprodusent(models.Model):
    navn = models.CharField(max_length=200)
    wikipedia = models.URLField(max_length=200, blank=True, null=True,
                                help_text='Link til wikipediaartikkel om selskapet')
    se_ogsa = \
        models.ManyToManyField('self', blank=True, verbose_name='Se også', help_text='Hold inne ctrl for å velge flere')
    lagt_til = models.DateTimeField(auto_now_add=True)
    endret = models.DateTimeField(auto_now=True)
    lagt_til_av =\
        models.ForeignKey('auth.User',
                          on_delete=models.PROTECT,
                          related_name='Chassisprodusent_Lagt_til_av')
    endret_av =\
        models.ForeignKey('auth.User',
                          on_delete=models.PROTECT,
                          related_name='Chassisprodusent_Endret_av',
                          null=True, blank=True)

    class Meta:
        verbose_name_plural = 'chassisprodusenter'
        ordering = ['navn']

    def __str__(self):
        return str(self.navn)

    def link(self):
        if self.navn.find('/') == -1:
            return self.navn
        else:
            return self.id

    def kan_endre(self, user):
        return utils.can_edit(self.lagt_til_av, user, 'bussdatabase.change_chassisprodusent')

    def bevarte_busser(self):
        from bussdatabase.models import Buss
        return Buss.objects.filter(chassisprodusent=self)

    def antall_bevarte(self):
        return self.bevarte_busser().count()


class Status(models.Model):
    navn = models.CharField(max_length=50)

    def __str__(self):
        return str(self.navn)

    class Meta:
        verbose_name_plural = 'statuser'


class Tilstand(models.Model):
    navn = models.CharField(max_length=50)

    def __str__(self):
        return str(self.navn)

    class Meta:
        verbose_name_plural = 'tilstander'


class Forening(models.Model):
    navn = models.CharField(max_length=100)
    sted = models.CharField(max_length=100)
    nettside = models.URLField()
    beskrivelse = models.TextField()
    logo = models.ImageField(upload_to='foreningslogoer/',
                             null=True, blank=True)
    leder = models.ForeignKey('auth.User',
                              on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.navn, self.sted)

    def kan_endre(self, user):
        return utils.can_edit(self.leder, user, 'bussdatabase.change_forening')

    class Meta:
        verbose_name_plural = 'foreninger'
