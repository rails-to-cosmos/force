from django.conf.urls import url, include
import views


urlpatterns = [
    url(r'^view/$', views.view_menu, name='menuview'),
    url(r'^load/', views.load_menu, name='menuload'),
]
