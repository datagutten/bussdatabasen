from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from bussdatabase.forms import VegvesenImportForm, VegvesenImportFormDiff
from bussdatabase.models import Buss


def import_vegvesen(regnr, user=None, save=True):
    import vegvesen
    opplysninger = vegvesen.opplysninger(regnr)
    buss = Buss.objects.get(registreringsnummer=regnr)
    if not buss:
        buss = Buss
        buss.registreringsnummer = regnr

    if not buss.chassistype and 'modell' in opplysninger:
        buss.chassistype = opplysninger['modell']
    if not buss.understellsnummer:
        buss.understellsnummer = opplysninger.get('understellsnr', None)
    if not buss.vekt and 'egenvekt' in opplysninger:
        buss.vekt = int(opplysninger['egenvekt'])
    if not buss.lengde and 'lengde' in opplysninger:
        buss.lengde = int(opplysninger['lengde']) / 100
    if not buss.bredde and 'bredde' in opplysninger:
        buss.bredde = int(opplysninger['bredde']) / 100
    if not buss.byggeår and 'registreringsaar' in opplysninger:
        buss.byggeår = int(opplysninger['registreringsaar'])
    if not buss.ståplasser:
        buss.ståplasser = opplysninger.get('staaplasser', None)
    if not buss.sitteplasser:
        buss.sitteplasser = opplysninger.get('seter', None)
    if user:
        buss.endret_av = user
    if save:
        buss.save()
    else:
        return buss


@login_required
def vegvesen_diff(request, regnr):
    import vegvesen
    opplysninger = vegvesen.opplysninger(regnr)
    # buss_db = Buss.objects.get(registreringsnummer=regnr)
    buss_db = get_object_or_404(Buss, registreringsnummer=regnr)

    if 'feilmelding' in opplysninger:
        print(opplysninger.get('feilmelding'))
        context = {'vegvesen': opplysninger, 'buss': buss_db}
    else:
        buss = Buss(registreringsnummer=regnr)
        if 'modell' in opplysninger:
            buss.chassistype = opplysninger['modell']
        buss.understellsnummer = opplysninger.get('understellsnr', None)
        if 'egenvekt' in opplysninger:
            buss.vekt = int(opplysninger['egenvekt'])
        if 'lengde' in opplysninger:
            buss.lengde = int(opplysninger['lengde']) / 100
        if 'bredde' in opplysninger:
            buss.bredde = int(opplysninger['bredde']) / 100
        if 'registreringsaar' in opplysninger:
            buss.byggeår = int(opplysninger['registreringsaar'])

        buss.ståplasser = opplysninger.get('staaplasser', None)
        buss.sitteplasser = opplysninger.get('seter', None)

        form = VegvesenImportFormDiff(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                import_vegvesen(form.cleaned_data['regnr'], request.user)
                return redirect('bussdatabase:buss_regnr',
                                regnr=form.cleaned_data['regnr'])

        fields = ['chassistype', 'vekt', 'lengde', 'bredde', 'byggeår', 'ståplasser', 'sitteplasser']
        context = {'buss': buss_db,
                   'vegvesen': opplysninger,
                   'buss_vegvesen': buss,
                   'fields': fields,
                   'form': form,
                   }
    return render(request, 'bussdatabase/import_vegvesen_diff.html', context)


@login_required
def import_vegvesen_quiet(request, regnr):
    import_vegvesen(regnr, request.user)
    return redirect('bussdatabase:buss_regnr', regnr=regnr)


@login_required
def import_vegvesen_form(request):
    form = VegvesenImportForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            import_vegvesen(form.cleaned_data['regnr'], request.user)
            return redirect('bussdatabase:buss_regnr',
                            regnr=form.cleaned_data['regnr'])
    context = {'form': form}
    return render(request, 'bussdatabase/import_vegvesen.html', context)
