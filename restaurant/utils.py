from django.utils import timezone
from models import Menu


def user_wants_actual_menu(request):
    return request.GET.get('menu', '') == 'actual'


def user_filter_by_category(request):
    return 'category' in request.GET


def get_actual_menu():
    return Menu.objects.filter(date__gte=timezone.now()).order_by('date')[0]
