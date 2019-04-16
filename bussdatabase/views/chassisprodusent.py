from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

import bussdatabase.views.generic
from bussdatabase.models import Chassisprodusent, Buss


def chassisprodusent(request, navn):
    print('Chassisprodusent')
    chassis_object = get_object_or_404(Chassisprodusent, navn=navn)
    busser = Buss.objects.filter(chassisprodusent=chassis_object)
    title = 'Busser fra %s' % chassis_object
    context = {'chassisprodusent': chassis_object, 'busser': busser, 'title': title,
               'kan_endre': chassis_object.kan_endre(request.user)}
    return render(request, 'bussdatabase/chassisprodusent.html', context)


@login_required
def chassisprodusent_form(request, navn=None):
    from bussdatabase.views import other
    return bussdatabase.views.generic.form(request, 'chassisprodusent', navn)

