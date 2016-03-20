from django.conf.urls import url
from views import authByUsername, logout_view

urlpatterns = [
    url(r'^$', authByUsername),
    url(r'^logout$', logout_view)
]
