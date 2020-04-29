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

    if request.method == 'OPTIONS':
        print('GOT OPTIONS')
        return HttpResponse('Success', status=204)

    # Getting Feature(s) from DB
    elif request.method == 'GET':

        # Given a single Feature based on ID
        if request.GET.get('id', ''):
            id = request.GET.get('id', '')
            feature = Feature.objects.filter(id=id).values()
            feat_json = feature_to_json(feature[0])

            return JsonResponse(feat_json)

        # All Features if no ID is given
        else:
            features = Feature.objects.all()
            feat_json = {}
            for f in features:
                feat_json[f.id] = feature_to_json(f)

            return JsonResponse(feat_json)

    # Creating a new Feature
    elif request.method == 'POST':
        print(request.POST.get('id', ''))
        # id = request.POST.get('id', '')
        # name = request.POST.get('name', '')
        # percent = request.POST.get('percent', '')
        # enabled = request.POST.get('enabled', '')
        #
        # new_feature = Feature(id, name, percent, enabled)
        #
        # new_feature.save()

        return HttpResponse('Nice', status=200)

    # Updating an existing Feature
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

    # Deletes an existing Feature
    elif request.method == 'DELETE':
        id = request.GET.get('id', '')
        Feature.objects.filter(id=id).delete()

        return HttpResponse('Nice', status=200)


# Converts a single Feature object to JSON
def feature_to_json(feat):

    fj = {
        'id': feat.id,
        'name': feat.name,
        'percent': feat.percent,
        'enabled': feat.enabled
    }

    return fj

