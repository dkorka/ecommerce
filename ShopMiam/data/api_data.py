from django.http import HttpResponse
from .models import Annonces
from django.core import serializers


def api_data(request):

    annonces = Annonces.objects.all()
    json = serializers.serialize("json", annonces)

    return HttpResponse(json)
