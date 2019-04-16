from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

import bussdatabase.views.generic
from bussdatabase.models import Selskap, Buss


def selskap(request, navn):
    selskap_object = get_object_or_404(Selskap, navn=navn)
    busser = Buss.objects.filter(selskap=selskap_object)
    title = 'Busser fra %s' % selskap_object
    context = {'selskap': selskap_object, 'busser': busser, 'title': title,
               'kan_endre': selskap_object.kan_endre(request.user)}
    return render(request, 'bussdatabase/selskap.html', context)


@login_required
def selskap_form(request, navn=None):
    from bussdatabase.views import other
    return bussdatabase.views.generic.form(request, 'selskap', navn)
