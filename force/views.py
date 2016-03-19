from django.http import HttpResponse
from django.template import loader, Context


def index(request):
    template = loader.get_template('index.html')
    context = Context({
        'userId': request.user.id,
    })
    return HttpResponse(template.render(context))
