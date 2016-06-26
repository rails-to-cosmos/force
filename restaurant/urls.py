import views

from django.conf.urls import url


urlpatterns = [
    url(r'^menu/load', views.load_menu),
    url(r'^menu/get', views.get_menu),
]
