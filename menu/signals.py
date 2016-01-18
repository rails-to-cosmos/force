from django.dispatch import Signal

load = Signal(providing_args=['file'])
order = Signal(providing_args=['user', 'menu', 'product'])
unorder = Signal(providing_args=['user', 'menu', 'product'])
build_order = Signal(providing_args=['menu'])
send_order = Signal(providing_args=['menu'])
