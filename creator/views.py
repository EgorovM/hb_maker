from django.shortcuts import render
from django.http import HttpResponse

from creator import models as ms


def index(request):
    return HttpResponse('хелло!')


def suprize_landing(request, keyword):
    landing = ms.SurprizeLanding.objects.get(keyword=keyword)

    return HttpResponse(landing.to_view())