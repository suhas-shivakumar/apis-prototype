from amadeus import Client, ResponseError
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.conf import settings
from . import token
import os
import requests
import urllib
from django.views.decorators.csrf import csrf_exempt

CLIENT_ID = "AMADEUS_CLIENT_ID"
CLIENT_SECRET = "AMADEUS_CLIENT_SECRET"

AMADEUS_CLIENT_ID = os.environ.get('AMADEUS_CLIENT_ID', None)
AMADEUS_CLIENT_SECRET = os.environ.get('AMADEUS_CLIENT_SECRET', None)

def prediction(request):
    origin = request.POST.get("Origin", None)
    destination = request.POST.get("Destination", None)
    if origin is None or destination is None:
        return render(request, 'demo_form.html', {})
    else:
        kwargs = {'originLocationCode': request.POST.get('Origin'),
                'destinationLocationCode': request.POST.get('Destination'),
                'departureDate': request.POST.get('Departuredate'),
                'returnDate': request.POST.get('Returndate')}
        try:
            purpose = amadeus.travel.predictions.trip_purpose.get(
                **kwargs).data['result']
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
            return render(request, 'demo_form.html', {})
        return render(request, 'index.html', {'message': 'The purpose of the requested trip is','result': purpose})

@csrf_exempt
def verify(request: HttpRequest) -> HttpResponse:
    client_id = request.POST.get("client_id", None)
    client_secret = request.POST.get("client_secret", None)
    method = request.POST.get("method", None)

    if client_id is not None and client_secret is not None:
        os.environ[CLIENT_ID] = client_id
        os.environ[CLIENT_SECRET] = client_secret
        global amadeus
        amadeus = Client()
        if method == "manual":
            return manual_request(request)
        return prediction(request)
    else:
        return HttpResponseRedirect('../')

def build_url( url: str, params: dict ):
    split_url = urllib.parse.urlsplit(url)
    split_url = split_url._replace(query=urllib.parse.urlencode(params))

    return urllib.parse.urlunsplit(split_url)

def manual_request(request):
    url = settings.TRIP_PURPOSE_API
    origin = request.POST.get("Origin", None)
    destination = request.POST.get("Destination", None)
    if origin is None or destination is None:
        return render(request, 'demo_form.html', {})
    else:
        params = {'originLocationCode': origin,
                'destinationLocationCode': destination,
                'departureDate': request.POST.get('Departuredate'),
                'returnDate': request.POST.get('Returndate')}

        access_token = token.get_token(os.environ.get(CLIENT_ID), os.environ.get(CLIENT_SECRET), False)['access_token']
        headers = {
            "cache-control": "no-cache",
            "Authorization": f"Bearer {access_token}"
        }

        api_url = build_url(url, params)
        response = requests.get(api_url, headers=headers, verify=False)
        if response.json() is not None:
            purpose = response.json()["data"]["result"]
            if purpose is not None:
                return render(request, 'index.html', {'message': 'The purpose of the requested trip is','result': purpose})
            else:
                return HttpResponse(response.text)
