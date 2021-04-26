# -*- coding: utf-8 -*-
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from bussdatabase.forms import BussForm
from bussdatabase.models import Bilde, Buss, Chassisprodusent, Karosserifabrikk, Selskap, Status, Tilstand


# https://djangosnippets.org/snippets/1474/
def get_referer_view(request, default=None):
    import re
    '''
    Return the referer view of the current request

    Example:

        def some_view(request):
            ...
            referer_view = get_referer_view(request)
            return HttpResponseRedirect(referer_view, '/accounts/login/')
    '''

    # if the user typed the url directly in the browser's address bar
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return default

    # remove the protocol and split the url at the slashes
    referer = re.sub('^https?:\/\/', '', referer).split('/')
    if referer[0] != request.META.get('SERVER_NAME'):
        return default

    # add the slash at the relative path's view and finished
    referer = u'/' + u'/'.join(referer[1:])
    return referer


def index(request, id=None, regnr=None, navn=None):
    from django.db.models import Q
    buss = Buss.objects.prefetch_related('images').\
        select_related('karosserifabrikk', 'chassisprodusent', 'selskap')
    if id or (navn and navn.isdigit()):
        buss = get_object_or_404(buss, id=id)
    elif navn:
        buss = get_object_or_404(buss,
                                 Q(registreringsnummer=navn) |
                                 Q(internnummer=navn))
    elif regnr:
        buss = get_object_or_404(buss, registreringsnummer=regnr)
    else:
        return

    context = {'buss': buss,
               'top_image': buss.toppbilde(),
               'title': buss.navn,
               'kan_endre': buss.kan_endre(request.user),
               'referer': get_referer_view(request,
                                           'bussdatabase:busstabell')}
    return render(request, 'bussdatabase/buss.html', context)


# https://stackoverflow.com/a/45139393/2630074
@login_required
def buss_ny(request):
    if request.method == 'POST':
        form = BussForm(request.POST)
        if form.is_valid():
            buss = form.save(commit=False)
            buss.lagt_til_av = request.user
            buss.endret_av = request.user
            buss.status = Status(pk=4)
            buss.save()
            if buss.registreringsnummer:
                return redirect('bussdatabase:buss_regnr',
                                regnr=buss.registreringsnummer)
            else:
                return redirect('bussdatabase:buss_id', id=buss.id)
    else:
        form = BussForm()
    context = {'form': form, 'title': 'Ny buss'}
    return render(request, 'bussdatabase/buss_ny.html', context)


@login_required
def buss_endre(request, id=None, regnr=None):
    from django.forms.models import model_to_dict
    # https://stackoverflow.com/a/4674127/2630074
    buss = False
    if id:
        buss = get_object_or_404(Buss, pk=id)
    elif regnr:
        buss = get_object_or_404(Buss, registreringsnummer=regnr)

    if not buss.kan_endre(request.user):
        return redirect(request.META['HTTP_REFERER'])

    form = BussForm(request.POST or None, instance=buss)

    if request.method == 'POST':

        if form.is_valid():
            dict = model_to_dict(buss)

            buss = form.save(commit=False)
            buss.endret_av = request.user
            buss.save()
            # buss.published_date = timezone.now()
            if buss.registreringsnummer:
                return redirect('bussdatabase:buss_regnr',
                                regnr=buss.registreringsnummer)
            else:
                return redirect('bussdatabase:buss_id', id=buss.id)
    context = {'form': form, 'buss': buss, 'title': 'Endre %s' % buss.navn}
    return render(request, 'bussdatabase/buss_ny.html', context)


def busstabell(request, selskap=None, merke=None, karosserifabrikk=None, chassis=None, eier=None, camping=False):
    vehicles = Buss.objects.prefetch_related('images').select_related('chassisprodusent', 'karosserifabrikk', 'selskap')
    if selskap:
        vehicles = vehicles.filter(selskap__navn=selskap)
        title = 'Busser fra %s' % selskap
    elif merke:
        vehicles = vehicles.filter(chassisprodusent__navn=merke)
        title = 'Busser med %s chassis' % merke
    elif karosserifabrikk:
        karosserifabrikk_object = get_object_or_404(Karosserifabrikk, forkortelse=karosserifabrikk)
        vehicles = vehicles.filter(karosserifabrikk=karosserifabrikk_object)
        title = 'Busser med karosseri fra %s' % karosserifabrikk_object.navn
    elif eier:
        vehicles = vehicles.filter(eier=eier)
        title = 'Busser eid av %s' % eier
    elif camping:
        vehicles = vehicles.filter(tilstand__navn='Campinginnredet')
        title = 'Busser med campinginnredning'
    else:
        vehicles = vehicles.order_by('byggeår')
        title = 'Bevarte busser'

    vehicles = vehicles.exclude(tilstand__navn='Hogget')

    context = {'busser': vehicles, 'bilder': Bilde, 'title': title}
    return render(request, 'bussdatabase/busser.html', context)


def busstabell_camping(request):
    return busstabell(request, camping=True)


def eiere(request):
    eierliste = Buss.objects.order_by('eier').values_list('eier', flat=True).distinct().exclude(eier=None)
    return render(request, 'bussdatabase/eiere.html', {'eiere': eierliste})
