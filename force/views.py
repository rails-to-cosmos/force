from django.http import HttpResponse
from django.template import loader
from menu.views import view_menu


def index(request):
    menu_data = view_menu(request).content
    template = loader.get_template('index.html')
    context = {
        u'userId': request.user.id,
        u'menuData': menu_data,
    }
    return HttpResponse(template.render(context))
