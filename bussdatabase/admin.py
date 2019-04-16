from django.contrib import admin

# Register your models here.
from .models import *


class BussAdmin(admin.ModelAdmin):
    list_display = ('navn', 'registreringsnummer', 'karosserifabrikk', 'vekt_tonn')


admin.site.register(Buss, BussAdmin)


class KaroserrifabrikkAdmin(admin.ModelAdmin):
    list_display = ('navn', 'forkortelse', 'sted')


admin.site.register(Karosserifabrikk, KaroserrifabrikkAdmin)

admin.site.register(Chassisprodusent)
admin.site.register(Selskap)


class BildeAdmin(admin.ModelAdmin):
    list_display = ('bussnavn', 'filnavn', 'toppbilde', 'lagt_til')


admin.site.register(Bilde, BildeAdmin)
admin.site.register(Status)
admin.site.register(Tilstand)
# https://stackoverflow.com/questions/16307307/django-admin-show-image-from-imagefield
