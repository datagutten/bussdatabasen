from django.urls import path, re_path

import bussdatabase.views.selskap
import bussdatabase.views.vegvesen
import bussdatabase.views.chassisprodusent
import bussdatabase.views.generic
from . import views

app_name = 'bussdatabase'
urlpatterns = [
    path('', views.busstabell, name='index'),
    path('buss', views.busstabell, name='index'),
    path('user', views.user, name='user'),
    path('accounts/profile/', views.user, name='user_profile'),
    # path('accounts/', include('django.contrib.auth.urls')),

    # path('buss/endre/<int:id>', views.buss_endre, name='endre_buss'),
    # path('buss/endre/<str:regnr>', views.buss_endre, name='endre_buss_regnr'),
    # Skjema buss
    path('buss/ny', views.buss.buss_ny, name='ny_buss'),
    path('buss/<int:id>/endre', views.buss.buss_endre, name='buss_endre_id'),
    path('buss/<str:regnr>/endre', views.buss.buss_endre, name='buss_endre'),
    # Bilder
    path('buss/<int:id>/bilder', views.buss_bilder, name='buss_bilder_id'),
    path('buss/<str:regnr>/bilder', views.buss_bilder, name='buss_bilder'),
    path('bilde/endre/<int:bilde_pk>', views.buss_bilder, name='bilde_endre'),
    path('bilde/exif/<int:bilde_pk>', views.bilde.exif, name='exif'),
    # Vis en enkelt buss
    path('buss/<int:id>', views.buss.index, name='buss_id'),
    path('buss/<str:navn>', views.buss.index, name='buss'),
    path('buss/<str:selskap> <str:internnummer>', views.buss.index, name='buss_internnummer'),
    path('buss/<str:regnr>', views.buss.index, name='buss_regnr'),

    # Busstabell
    path('busser', views.busstabell, name='busstabell'),
    path('campingbusser', views.busstabell_camping, name='busstabell_camping'),
    path('buss', views.busstabell),

    re_path(r'busser/selskap/(?P<navn>.+)$', bussdatabase.views.selskap.selskap, name='busstabell_selskap'),
    path('busser/merke/<str:merke>', views.busstabell, name='busstabell_merke'),
    path('busser/chassis/<str:chassis>', views.busstabell, name='busstabell_chassis'),
    path('busser/karosseri/<str:karosserifabrikk>', views.busstabell, name='busstabell_karosseri'),
    re_path(r'busser/eier/(?P<eier>.+)$', views.busstabell, name='busstabell_eier'),
    # Karosseri
    path('karosserifabrikker', views.karosserifabrikker, name='karosserifabrikker'),
    path('karosserifabrikk/ny', views.karosserifabrikk_form, name='karosserifabrikk_ny'),
    re_path(r'^karosserifabrikk/endre/(?P<navn>.+)$', views.karosserifabrikk_form, name='karosserifabrikk_endre'),
    re_path(r'^karosserifabrikk/(?P<navn>.+)$', views.karosserifabrikk, name='karosserifabrikk'),

    # Import
    path('import/vegvesen/<str:regnr>', bussdatabase.views.vegvesen.import_vegvesen_quiet, name='import_vegvesen_quiet'),
    path('import/vegvesen', bussdatabase.views.vegvesen.import_vegvesen_form, name='import_vegvesen_form'),
    path('import/vegvesen/<str:regnr>/diff', bussdatabase.views.vegvesen.vegvesen_diff, name='import_vegvesen_diff'),
    # Problemer
    path('problemer/manglende_fotograf', views.manglende_fotograf, name='manglende_fotograf'),
    # Selskap
    path('selskap/ny', bussdatabase.views.selskap.selskap_form, name='selskap_ny'),
    # path('selskap/endre/<str:navn>', bussdatabase.views.selskap.selskap_form, name='selskap_endre'),
    re_path(r'^selskap/endre/(?P<navn>.+)$', bussdatabase.views.selskap.selskap_form, name='selskap_endre'),
    re_path(r'^selskap/(?P<navn>.+)$', bussdatabase.views.selskap.selskap, name='selskap'),
    path('eiere', views.eiere, name='eiere'),


    # path('chassisprodusenter', views.chassisprodusent.chassisprodusenter, name='chassisprodusent'),
    # Generic
    re_path(r'^firma/(?P<topic>[^/]+)$', bussdatabase.views.generic.list_all, name='generic_list_all'),
    re_path(r'^firma/(?P<topic>[^/]+)/ny$', bussdatabase.views.generic.form, name='generic_ny'),
    re_path(r'^firma/(?P<topic>[^/]+)/(?P<navn>.+)$', bussdatabase.views.generic.list_topic, name='generic_list'),
    re_path(r'^firma/(?P<topic>[^/]+)/endre/(?P<navn>.+)$', bussdatabase.views.generic.form, name='generic_endre'),
    # Chassis
    path('firma/chassisprodusent/<str:navn>', views.chassisprodusent.chassisprodusent, name='chassisprodusent'),
    path('chassisprodusent/<str:navn>', views.chassisprodusent.chassisprodusent),

    # re_path(r'^(?P<topic>.+?)/ny$', bussdatabase.views.generic.form),


]
