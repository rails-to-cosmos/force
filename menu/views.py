from django.http import HttpResponse
from django.template import loader


def load_menu(request):
    template = loader.get_template('menu/load.html')

    def post(x): return request.POST.get(x, False)

    context = {
        'success': post('success'),
        'error': post('error')
    }

    if request.method == 'POST':
        pass

    return HttpResponse(template.render(context, request))


def view_menu(request):
    return HttpResponse('Menu view page')
