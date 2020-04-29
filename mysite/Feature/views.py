# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.http import JsonResponse

import json

from .models import Feature


# Create your views here.

@csrf_exempt
def index(request):

    if request.method == 'OPTIONS':
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
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        for key in body:
            feat = body[key]
            id = feat['id']
            name = feat['name']
            percent = feat['percent']
            enabled = feat['enabled']

            new_feature = Feature(id, name, percent, enabled)

            new_feature.save()

        return HttpResponse('Nice', status=200)

    # Updating an existing Features
    elif request.method == 'PATCH':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body['id']

        feature_to_update = Feature.objects.get(id=id)

        try:
            feature_to_update.name = body['name']
        except KeyError:
            pass

        try:
            feature_to_update.percent = body['percent']
        except KeyError:
            pass

        try:
            feature_to_update.enabled = body['enabled']
        except KeyError:
            pass


        feature_to_update.save()

        return HttpResponse('Nice', status=200)

    # Deletes an existing Feature
    elif request.method == 'DELETE':
        id = request.GET.get('id', '')
        Feature.objects.filter(id=id).delete()

        return HttpResponse('Nice', status=200)


# Finds feature given its name
def search(request):
    if request.method == "GET":
        name = request.GET.get('name', '')

        features = Feature.objects.filter(name=name)

        feat_json = {}
        for f in features:
            feat_json[f.id] = feature_to_json(f)

        return JsonResponse(feat_json)


# Converts a single Feature object to JSON
def feature_to_json(feat):

    fj = {
        'id': feat.id,
        'name': feat.name,
        'percent': feat.percent,
        'enabled': feat.enabled
    }

    return fj

