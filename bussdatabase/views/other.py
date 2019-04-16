# Create your views here.
from bussdatabase.models import Buss

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def user(request):

    context = {
        'user': request.user,
        'busser': Buss.objects.filter(lagt_til_av=request.user),
    }

    return render(request, 'bussdatabase/profile.html', context)


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


