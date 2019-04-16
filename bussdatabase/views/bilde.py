from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from bussdatabase.models import Bilde, Buss
from bussdatabase.forms import BussBildeForm, BussBildeEndreForm


def host(request):
    return request.scheme + '://' + request.get_host()


def rotate_image(filepath):
    # https://stackoverflow.com/a/26928142/2630074
    from PIL import Image, ExifTags
    try:
        image = Image.open(filepath)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        else:
            return
        image.save(str(filepath))
        image.close()

    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass


@login_required
def buss_bilder(request, pk=False, id=False, regnr=False, bilde_pk=None):
    bilde = None
    if regnr:
        buss_object = get_object_or_404(Buss, registreringsnummer=regnr)
    elif pk:
        buss_object = get_object_or_404(Buss, pk=pk)
    elif id:
        buss_object = get_object_or_404(Buss, pk=id)
    elif bilde_pk:
        bilde = Bilde.objects.get(pk=bilde_pk)
        buss_object = bilde.buss
    else:
        raise ValueError('Hverken id eller regnr er satt')

    bilder = Bilde.objects.filter(buss=buss_object)
    if request.method == 'POST':
        if not bilde:
            form = BussBildeForm(request.POST, request.FILES)
        else:
            form = BussBildeEndreForm(request.POST, request.FILES, instance=bilde)
        if form.is_valid():
            bilde = form.save(commit=False)
            bilde.buss = buss_object
            # Sjekk om bildet skal være toppbilde
            # Finn eksisterende toppbilde(r)
            toppbilde = Bilde.objects.filter(buss=buss_object,
                                             toppbilde=True)
            if bilde.toppbilde:
                # Fjern eksisterende toppbilde
                if toppbilde:
                    toppbilde.update(toppbilde=False)
            else:
                # Sørg for at det er et toppbilde
                if not toppbilde:
                    bilde.toppbilde=True
            bilde.lagt_til_av = request.user
            bilde.endret_av = request.user

            bilde.save()
            if not bilde_pk:
                rotate_image(bilde.bilde)
            return redirect(request.META['HTTP_REFERER'])
        else:
            print(form.errors)
    elif bilde_pk:  # Endre bilde
        form = BussBildeEndreForm(instance=bilde)
    else:  # Nytt bilde
        form = BussBildeForm()
    context = {'form': form,
               'buss': buss_object,
               'bilder': bilder,
               'bilde': bilde,
               'host': host(request)
               }
    return render(request, 'bussdatabase/buss_bilder.html', context)


def exif(request, bilde_pk):
    bilde_object = get_object_or_404(Bilde, pk=bilde_pk)
      
    # https://stackoverflow.com/a/26928142/2630074
    from PIL import Image, ExifTags
    # try:
    image = Image.open(bilde_object.bilde.name)

    info = dict()

    try:
        for tag, value in image._getexif().items():
            if tag not in ExifTags.TAGS:
                name = tag
            else:
                name = ExifTags.TAGS[tag]
            info[name] = value
    except AttributeError:
        pass

    image.close()
    context = {'exif': info.items(),
               'bilde': bilde_object, }
    return render(request, 'bussdatabase/exif.html', context)


def manglende_fotograf(request):
    bilder = Bilde.objects.filter(fotograf=None)
    context = {'bilder': bilder}
    return render(request, 'bussdatabase/bildeliste.html', context)
