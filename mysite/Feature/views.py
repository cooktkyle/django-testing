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
        new_feature = Feature(id, name, percent, enabled)
        new_feature.save()
        return HttpResponse('Nice', status=200)
    elif request.method == 'PATCH':
        id = request.GET.get('id', '')
        feature_to_update = Feature.objects.get(id=id)

        if request.GET.get('name', ''):
            feature_to_update.name = request.GET.get('name', '')
        if request.GET.get('percent', ''):
            feature_to_update.percent = request.GET.get('percent', '')
        if request.GET.get('enabled', ''):
            feature_to_update.enabled = request.GET.get('enabled', '')

        feature_to_update.save()

        return HttpResponse('Nice', status=200)
    elif request.method == 'DELETE':
        id = request.GET.get('id', '')
        Feature.objects.filter(id=id).delete()

        return HttpResponse('Nice', status=200)
