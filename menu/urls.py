import views

from django.conf.urls import url


urlpatterns = [
    url(r'^view/$', views.view_menu),
    url(r'^load/', views.load_menu),
]
