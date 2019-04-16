from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class BussForm(forms.ModelForm):

    class Meta:
        model = Buss
        '''fields = (  'selskap',
                    'internnummer',
                    'registreringsnummer',
                    'understellsnummer',
                    'opprinnelig_registreringsnummer',
                    'chassisprodusent',
                    'chassistype',
                    'karosserifabrikk',
                    'karosseritype',
                    'motor',
                    'ytelse',
                    'eier',
                    'byggeår',
                    'lengde',
                    'bredde',
                    'vekt',
                    'akselavstand',
                    'sitteplasser',
                    'ståplasser',
                    'tilstand',
                    'tittel',
                    'beskrivelse',
                    'merknad',)'''
        exclude = ('status', 'lagt_til_av', 'endret_av')
# class BussBildeForm(forms.Form):
#    title = forms.CharField(max_length=50)
#    bilde = forms.FileField()


class BussBildeForm(forms.ModelForm):
    class Meta:
        model = Bilde
        # fields = ('bilde', 'bildetekst', 'fotograf')
        exclude = ('buss', 'lagt_til_av', 'endret_av')

        
class BussBildeEndreForm(forms.ModelForm):
    class Meta:
        model = Bilde
        # fields = ('bilde', 'bildetekst', 'fotograf')
        exclude = ('buss', 'bilde', 'lagt_til_av', 'endret_av')

        
class VegvesenImportForm(forms.Form):
    regnr = forms.CharField(label='Registreringsnummer', max_length=8)


class VegvesenImportFormDiff(forms.Form):
    byggear = forms.BooleanField(label='Byggeår', required=False)
    chassis = forms.BooleanField(label='Chassistype', required=False)
    ytelse = forms.BooleanField(label='Ytelse (Hk)', required=False)
    lengde = forms.BooleanField(label='Lengde', required=False)
    bredde = forms.BooleanField(label='Bredde', required=False)
    akselavstand = forms.BooleanField(label='Akselstand', required=False)
    vekt = forms.BooleanField(label='Egenvekt', required=False)
    sitteplasser = forms.BooleanField(label='Sitteplasser', required=False)
    staplasser = forms.BooleanField(label='Ståplasser', required=False)


class SelskapForm(forms.ModelForm):
    class Meta:
        model = Selskap
        exclude = {'lagt_til', 'endret', 'lagt_til_av', 'endret_av'}


class KarosserifabrikkForm(forms.ModelForm):
    class Meta:
        model = Karosserifabrikk
        exclude = {'lagt_til', 'endret', 'lagt_til_av', 'endret_av'}


class ChassisForm(forms.ModelForm):
    class Meta:
        model = Chassisprodusent
        exclude = {'lagt_til', 'endret', 'lagt_til_av', 'endret_av'}


class GenericForm(forms.ModelForm):
    #self._meta.model
    class Meta:
        # model = None
        exclude = {'lagt_til', 'endret', 'lagt_til_av', 'endret_av'}
