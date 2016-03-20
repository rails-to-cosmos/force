from django.http import HttpResponse
from django.template import loader
from menu.views import view_menu


def index(request):
    menu_data = view_menu(request).content
    template = loader.get_template('index.html')

    context = {
        u'user': {
            u'id': request.user.id,
        },
        u'menuData': menu_data,
    }

    if request.user.id:
        context[u'user'][u'fullname'] = u'{first_name} {last_name}'.format(
            first_name=request.user.first_name,
            last_name=request.user.last_name
        )

    return HttpResponse(template.render(context))
