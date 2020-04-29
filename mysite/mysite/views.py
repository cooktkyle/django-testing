# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

@csrf_exempt
def index(request):
    print(request.method)
    return HttpResponse("Nyello")