from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse

# Create your views here.

def authByUsername(request):
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

    user = authenticate(username=username, password=password)
    if not user:
        response = JsonResponse({
            'error': 'Bad credentials',
            'user': username,
            'password': password
        })
        response.status_code = 401
        return response

    if user.is_active:
        login(request, user)
        response = JsonResponse({
            'success': 'Successfully authorized'
        })
        response.status_code = 200
        return response
    else:
        response = JsonResponse({
            'error': 'User is not active'
        })
        response.status_code = 403
        return response

def logout_view(request):
    logout(request)
    response = JsonResponse({
        'success': 'Successfully logged out'
    })
    response.status_code = 200
    return response
