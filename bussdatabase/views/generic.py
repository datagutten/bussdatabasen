from django.contrib.auth.decorators import login_required

from bussdatabase.forms import KarosserifabrikkForm, ChassisForm, SelskapForm, BussForm
from bussdatabase.models import Buss, Chassisprodusent, Karosserifabrikk, Selskap
from django.shortcuts import get_object_or_404, render, redirect


def select_topic(topic):
    if topic == 'karosserifabrikk':
        info = {
            'model': Karosserifabrikk,
            'title_new': 'Legg til ny karosserifabrikk',
            'redir': 'bussdatabase:karosserifabrikk',
            'form_obj': KarosserifabrikkForm
        }
    elif topic == 'chassisprodusent':
        info = {
            'model': Chassisprodusent,
            'title_new': 'Legg til ny chassisprodusent',
            'redir': 'bussdatabase:chassisprodusent',
            'form_obj': ChassisForm,
        }
    elif topic == 'selskap':
        info = {
            'model': Selskap,
            'title_new': 'Legg til nytt selskap',
            'redir': 'bussdatabase:selskap',
            'form_obj': SelskapForm,
        }
    elif topic == 'buss':
        info = {
            'model': Buss,
            'title_new': 'Legg til ny buss',
            'redir': 'bussdatabase:buss',
            'form_obj': BussForm,
            'template': 'bussdatabase/buss_form.html',
        }
    else:
        raise ValueError('Invalid topic')
    return info


def list_topic(request, topic, navn):
    # info = select_topic(topic)
    if topic == 'karosserifabrikk':
        import bussdatabase.views.karosserifabrikk as karosserifabrikk
        return karosserifabrikk.karosserifabrikk(request, navn)
    elif topic == 'chassisprodusent':
        from bussdatabase.views import chassisprodusent
        return chassisprodusent.chassisprodusent(request, navn)
    elif topic == 'selskap':
        from bussdatabase.views import selskap
        return selskap.selskap(request, navn)
    elif topic == 'buss':
        from bussdatabase.views import buss
        return buss.index(request, navn=navn)


def list_all(request, topic):
    info = select_topic(topic)
    model = info['model']

    objects = model.objects.all()
    context = {'objects': objects}
    return render(request, 'bussdatabase/list_all/%s.html' % topic, context)


@login_required
def form(request, topic, navn=None):
    template = None
    if topic == 'karosserifabrikk':
        model = Karosserifabrikk
        title_new = 'Legg til ny karosserifabrikk'
        redir = 'bussdatabase:karosserifabrikk'
        form_obj = KarosserifabrikkForm
    elif topic == 'chassisprodusent':
        model = Chassisprodusent
        title_new = 'Legg til ny chassisprodusent'
        redir = 'bussdatabase:chassisprodusent'
        form_obj = ChassisForm
    elif topic == 'selskap':
        model = Selskap
        title_new = 'Legg til nytt selskap'
        redir = 'bussdatabase:selskap'
        form_obj = SelskapForm
    elif topic == 'buss':
        model = Buss
        title_new = 'Legg til ny buss'
        redir = 'bussdatabase:buss'
        form_obj = BussForm
        template = 'bussdatabase/buss_form.html'
    else:
        raise ValueError('Invalid topic')

    if navn:
        if topic == 'buss':
            if navn.isdigit():
                obj = get_object_or_404(Buss, pk=navn)
            else:
                obj = get_object_or_404(Buss, registreringsnummer=navn)
        else:
            obj = get_object_or_404(model, navn=navn)

        if callable(obj.navn):
            title = 'Endre %s' % obj.navn()
            navn = obj.navn()
        else:
            title = 'Endre %s' % obj.navn
            navn = obj.navn

        if not obj.kan_endre(request.user):
            return redirect(redir, navn=navn)
    else:
        obj = None
        title = title_new

    form_obj = form_obj(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form_obj.is_valid():
            obj = form_obj.save(commit=False)
            if navn:
                obj.endret_av = request.user
            else:
                obj.lagt_til_av = request.user
            obj.save()
            form_obj.save_m2m()
            if callable(obj.navn):
                return redirect(redir, navn=obj.navn())
            else:
                return redirect(redir, navn=obj.navn)

    context = {'form': form_obj, 'title': title}
    return render(request,
                  template or 'bussdatabase/generic_form.html',
                  context)
