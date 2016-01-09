from django.shortcuts import render
from django.http import HttpResponse

def load_menu(request):
    return HttpResponse('Menu load page')

def view_menu(request):
    return HttpResponse('Menu view page')

# Create your views here.
