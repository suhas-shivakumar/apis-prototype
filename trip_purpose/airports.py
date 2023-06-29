from django.contrib import messages
from amadeus import Client, ResponseError, Location
from django.http import HttpResponse, HttpRequest
import json
import os

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
    global amadeus
    amadeus = Client()
    return origin_airport_search(request)