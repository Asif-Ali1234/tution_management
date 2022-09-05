from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
# Create your views here.

def root(requests):
    return redirect('/accounts/login/')
