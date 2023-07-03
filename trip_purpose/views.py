from amadeus import Client, ResponseError
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.conf import settings
from . import token
import os
import requests
import urllib

def prediction(request):
    origin = request.POST.get("Origin", None)
    destination = request.POST.get("Destination", None)
    if origin is None or destination is None:
        return render(request, 'trip_form.html', {})
    else:
        kwargs = {'originLocationCode': request.POST.get('Origin'),
                'destinationLocationCode': request.POST.get('Destination'),
                'departureDate': request.POST.get('Departuredate'),
                'returnDate': request.POST.get('Returndate')}
        try:
            purpose = amadeus.travel.predictions.trip_purpose.get(
                **kwargs).data['result']
        except ResponseError as error:
            purpose = manual_search_request(kwargs)
            if purpose is None:
                messages.add_message(request, messages.ERROR, error)
                return render(request, 'trip_form.html', {})
        return render(request, 'trip_index.html', {'message': 'The purpose of the requested trip is','result': purpose})

def verify(request: HttpRequest) -> HttpResponse:
    method = request.POST.get("method", None)
    if amadeus_status(request):
        return prediction(request)
    else:
        return HttpResponseRedirect('../')

def build_url( url: str, params: dict ):
    split_url = urllib.parse.urlsplit(url)
    split_url = split_url._replace(query=urllib.parse.urlencode(params))

    return urllib.parse.urlunsplit(split_url)

def manual_search_request(params):
    url = settings.TRIP_PURPOSE_API
    access_token = token.get_token(os.environ.get(settings.CLIENT_ID), os.environ.get(settings.CLIENT_SECRET), False)['access_token']
    headers = {
        "cache-control": "no-cache",
        "Authorization": f"Bearer {access_token}"
    }
    api_url = build_url(url, params)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.json() is not None:
        purpose = response.json()["data"]["result"]
        if purpose is not None:
            return purpose
        return None

def amadeus_status(request: HttpRequest):
    if settings.CLIENT_ID in request.session and settings.CLIENT_SECRET in request.session:
        os.environ[settings.CLIENT_ID] = request.session[settings.CLIENT_ID]
        os.environ[settings.CLIENT_SECRET] = request.session[settings.CLIENT_SECRET]
        global amadeus
        amadeus = Client()
        return True
    return False