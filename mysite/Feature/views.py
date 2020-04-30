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

        # Gather fields to validate
        features = Feature.objects.all()
        feature_IDs = []
        feature_names = []

        for f in features:
            feature_names.append(f.name)
            feature_IDs.append(f.id)

        # Get starting value for ID
        available_id = get_available_id(feature_IDs)

        invalid_features = {}
        created_features = {}

        # Iterate through post data
        for key in body:
            feat = body[key]

            # If the name is not unique, skip and add to return
            name = feat['name']
            if name in feature_names:
                invalid_features[key] = body[key]
                continue

            id = available_id
            # Deconstructs, increments, reconstructs
            available_id = 'F' + str(int(available_id[1:]) + 1)

            percent = feat['percent']
            enabled = feat['enabled']

            # Create, save, and add to return successful creation
            new_feature = Feature(id, name, percent, enabled)
            new_feature.save()
            created_features[new_feature.id] = feature_to_json(new_feature)

        # If there was unsuccessful Feature or all successful
        if len(invalid_features) > 0:
            return JsonResponse(invalid_features, status=207)
        else:
            return JsonResponse(created_features, status=201)

    # Updating an existing Features
    elif request.method == 'PATCH':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body['id']

        feature_to_update = Feature.objects.get(id=id)

        # Gather and update specified fields
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

        # Save and return
        feature_to_update.save()

        return JsonResponse(feature_to_json(feature_to_update), status=200)

    # Deletes an existing Feature
    elif request.method == 'DELETE':
        id = request.GET.get('id', '')
        Feature.objects.filter(id=id).delete()

        return HttpResponse('', status=205)


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


# Gets the next available id
def get_available_id(ids):
    if len(ids) == 0:
        return 'F0'
    else:
        # Ignoring leading F, incrementing, prepending F
        ids_as_numbers = [int(id[1:]) for id in ids]
        max_id = max(ids_as_numbers) + 1
        return 'F' + str(max_id)

