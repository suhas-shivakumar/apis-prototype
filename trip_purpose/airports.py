from django.contrib import messages
from amadeus import Client, ResponseError, Location
from django.http import HttpResponse, HttpRequest
import json
import os
from django.conf import settings

def origin_airport_search(request):
    if is_ajax(request=request):
        try:
            data = amadeus.reference_data.locations.get(keyword=request.GET.get('term', None),
                                                        subType=Location.ANY).data
            return HttpResponse(get_city_airport_list(data), 'application/json')
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)

def destination_airport_search(request):
    if is_ajax(request=request):
        try:
            data = amadeus.reference_data.locations.get(keyword=request.GET.get('term', None),
                                                        subType=Location.ANY).data
            return HttpResponse(get_city_airport_list(data), 'application/json')
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)

def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]['iataCode'] + ', ' + data[i]['name'])
    result = list(dict.fromkeys(result))
    return json.dumps(result)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def verify(request: HttpRequest) -> HttpResponse:
    if settings.CLIENT_ID in request.session and settings.CLIENT_SECRET in request.session:
        os.environ[settings.CLIENT_ID] = request.session[settings.CLIENT_ID]
        os.environ[settings.CLIENT_SECRET] = request.session[settings.CLIENT_SECRET]
        global amadeus
        amadeus = Client()
        return origin_airport_search(request)
    return "Credentials not found"