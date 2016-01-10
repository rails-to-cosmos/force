from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.view_menu, name='menuview'),
    url(r'^load/', views.load_menu, name='menuload'),
]
