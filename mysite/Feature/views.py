# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from .models import Feature


# Create your views here.

@csrf_exempt
def index(request):
    if request.method == 'GET':
        if request.GET.get('id', ''):
            id = request.GET.get('id', '')
            feature = Feature.objects.filter(id=id).values()
            return HttpResponse(feature)
        else:
            features = Feature.objects.all().values()
            return HttpResponse(features)
    elif request.method == 'POST':
        id = request.POST.get('id', '')
        name = request.POST.get('name', '')
        percent = request.POST.get('percent', '')
        enabled = request.POST.get('enabled', '')
        newFeature = Feature(id, name, percent, enabled)
        newFeature.save()
        return HttpResponse('Nice', status=200)
    elif request.method == 'PATCH:':
        
        return HttpResponse('Nice', status=200)
    elif request.method == 'DELETE':
        return HttpResponse(request.POST)
