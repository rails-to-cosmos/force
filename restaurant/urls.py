import views

from django.conf.urls import url


urlpatterns = [
    url(r'^load/', views.load_menu),
]
