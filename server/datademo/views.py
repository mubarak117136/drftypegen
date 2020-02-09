import logging
import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.views import View

from pprint import pprint, pformat

from . import serializers
from . import models
from drftypegen.drftypegen.compilers import *
logger = logging.getLogger(__name__)
from django.http import HttpResponse

import django.apps
from wagtail.core.models import Page

class DataDemo(APIView):
    def get(self, request):
        #wagtail adapter
        all_m = django.apps.apps.get_models()
        rel_m = [m for m in all_m if issubclass(m, Page) and m != Page]
        p = rel_m[0]
        wagtail_adapter = WagtailAdapter(p)
        data = wagtail_adapter.get_transformed_data()

        return Response({
            'status': status.HTTP_200_OK,
            'data': data
        })


def typescript_interface(request):
    tscompiler = TypeScriptCompiler()
    data = tscompiler.generate()

    #wagtail adapter
    all_m = django.apps.apps.get_models()
    rel_m = [m for m in all_m if issubclass(m, Page) and m != Page]
    p = rel_m[0]
    wagtail_adapter = WagtailAdapter(p)
    wagtail_adapter.get_transformed_data()

    return HttpResponse(data)

class List(ListAPIView):
    serializer_class = serializers.PersonSerializer

    def get_queryset(self):
        person = models.Person.objects.all()
        return person


