from django.http import HttpResponse
from django.template import loader, Context


def index(request):
    template = loader.get_template('index.html')
    context = Context({
        'app': 'force',
        'user': request.user,
        'ip_addr': request.META['REMOTE_ADDR'],
        'message': 'index view!'
    })
    return HttpResponse(template.render(context))
