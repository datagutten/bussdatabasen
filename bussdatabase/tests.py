from django.test import TestCase

from bussdatabase.models import Buss, Chassisprodusent, Karosserifabrikk, Selskap

from django.test.client import Client
from django.contrib.auth.models import User


def create_user():
    user = User.objects.create_user('test', 'test@bussdatabasen.no', 'secret')
    return user


def create_buss():
    selskap = Selskap.objects.create(navn='Oslo sporveier', forkortelse='OS')
    karosseri = Karosserifabrikk.objects.create(navn='Arna Busser AS',
                                                alternativt_navn='Arna Bruk',
                                                forkortelse='Arna',
                                                sted='Arna ved Bergen',
                                                første_år=1947,
                                                siste_år=1997)
    chassis = Chassisprodusent.objects.create(navn='Volvo',
                                              wikipedia='https://no.wikipedia.org/wiki/Volvo_Bussar')
    Buss.objects.create(selskap=selskap,
                        registreringsnummer='SR18712',
                        byggeår=1987,
                        karosserifabrikk=karosseri,
                        chassis=chassis,
                        motor='THB100EB',
                        ytelse=245,
                        lengde=12.2,
                        bredde=2.5,
                        akselavstand=5.9,
                        vekt=1070,
                        sitteplasser=38,
                        ståplasser=35,
                        eier='Lokaltrafikkhistorisk forening',
                        )


class BussTestCase(TestCase):
    def setUp(self):
        # self.user = create_user()
        # self.client = Client
        create_buss()

    def test_buss_navn(self):
        buss = Buss.objects.get(registreringsnummer='SR18712')
        print(buss)
        print(buss.navn())

        self.assertEqual(buss.navn(), 'Oslo sporveier 793')
        self.assertEqual(buss.navn_kort(), 'OS 793')
