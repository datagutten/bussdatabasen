from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

import bussdatabase.views.generic
from bussdatabase.forms import KarosserifabrikkForm
from bussdatabase.models import Buss, Karosserifabrikk


def karosserifabrikker(request, bevarte=None):
    fabrikker = Karosserifabrikk.objects.all()
    context = {'objects': fabrikker}
    return render(request, 'bussdatabase/list_all/karosserifabrikk.html', context)


def karosserifabrikk(request, navn):
    from django.db.models import Q
    if navn.isdigit():
        karosserifabrikk_object = get_object_or_404(Karosserifabrikk, id=int(navn))
    else:
        karosserifabrikk_object = get_object_or_404(Karosserifabrikk,
                                                    Q(navn=navn) |
                                                    Q(alternativt_navn=navn) |
                                                    Q(forkortelse=navn))

    # karosserifabrikk_object = karosserifabrikk_object.first()
    # karosserifabrikk_object = get_object_or_404(Karoserrifabrikk, navn=navn)
    busser = Buss.objects.filter(karosserifabrikk=karosserifabrikk_object)
    title = 'Busser fra %s' % karosserifabrikk_object
    context = {'karosserifabrikk': karosserifabrikk_object, 'busser': busser, 'title': title,
               'kan_endre': karosserifabrikk_object.kan_endre(request.user)}
    return render(request, 'bussdatabase/list/karosserifabrikk.html', context)


@login_required
def karosserifabrikk_form(request, navn=None):
    from bussdatabase.views import other
    return bussdatabase.views.generic.form(request, 'karosserifabrikk', navn)
