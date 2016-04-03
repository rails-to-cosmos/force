from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout

from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse


def login(request):
    if request.user.is_authenticated():
        response = JsonResponse({
            'error': 'Already authenticated'
        })
        response.status_code = 200
        return response

    try:
        username = request.POST['username']
        password = request.POST['password']
    except MultiValueDictKeyError:
        response = JsonResponse({
            'error': 'Specify username and password to continue'
        })
        response.status_code = 401
        return response

    user = django_authenticate(username=username, password=password)
    if not user:
        response = JsonResponse({
            'error': 'Bad credentials',
            'user': username,
            'password': password
        })
        response.status_code = 401
        return response

    if user.is_active:
        django_login(request, user)
        response = JsonResponse({
            'success': 'Successfully authorized',
            'fullname': u'{first_name} {last_name}'.format(
                first_name=user.first_name,
                last_name=user.last_name)
        })
        response.status_code = 200
        return response
    else:
        response = JsonResponse({
            'error': 'User is not active'
        })
        response.status_code = 403
        return response


def logout(request):
    django_logout(request)
    response = JsonResponse({
        'success': 'Successfully logged out'
    })
    response.status_code = 200
    return response
