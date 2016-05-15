from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User

from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse

from rest_framework import status


ERROR_KEY = 'error'
SUCCESS_KEY = 'success'


@ensure_csrf_cookie
def login(request):
    if request.user.is_authenticated():
        response = JsonResponse({
            ERROR_KEY: 'Already authenticated'
        })
        return response

    try:
        username = request.POST['username']
        password = request.POST['password']
    except MultiValueDictKeyError:
        response = JsonResponse({
            ERROR_KEY: 'Specify username and password to continue'
        }, status=status.HTTP_401_UNAUTHORIZED)
        return response

    user = django_authenticate(username=username, password=password)
    if not user:
        response = JsonResponse({
            ERROR_KEY: 'Bad credentials',
            'user': username,
            'password': password
        }, status=status.HTTP_401_UNAUTHORIZED)
        return response

    if user.is_active:
        django_login(request, user)
        response = JsonResponse({
            SUCCESS_KEY: 'Successfully authorized',
            'fullname': u'{first_name} {last_name}'.format(
                first_name=user.first_name,
                last_name=user.last_name)
        })
        return response
    else:
        response = JsonResponse({
            ERROR_KEY: 'User is not active'
        }, status=status.HTTP_403_FORBIDDEN)
        return response


@ensure_csrf_cookie
def logout(request):
    django_logout(request)
    response = JsonResponse({
        SUCCESS_KEY: 'Successfully logged out'
    })
    return response


def current_user(request):
    try:
        user = User.objects.filter(id=request.user.id)[0]
        response = JsonResponse({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })
    except IndexError:
        response = JsonResponse({
            'unauthorized': True
        })

    return response
