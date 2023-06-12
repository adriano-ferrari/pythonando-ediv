from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'register.html')
