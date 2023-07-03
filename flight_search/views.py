import json
import os
from django.conf import settings
from amadeus import Client, ResponseError, Location
from django.shortcuts import render
from django.contrib import messages
from .flight import Flight
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import requests
import logging

def demo(request):
    origin = request.POST.get('Origin')
    destination = request.POST.get('Destination')
    departureDate = request.POST.get('Departuredate')
    returnDate = request.POST.get('Returndate')
    adults = request.POST.get('Adults')

    if not adults:
        adults = 1

    kwargs = {'originLocationCode': origin,
              'destinationLocationCode': destination,
              'departureDate': departureDate,
              'adults': adults
              }

    tripPurpose = ''
    if returnDate:
        kwargs['returnDate'] = returnDate
        try:
            trip_purpose_response = amadeus.travel.predictions.trip_purpose.get(**kwargs).data
            tripPurpose = trip_purpose_response['result']
        except Exception as error:
            messages.add_message(request, messages.ERROR, error)
            return render(request, 'demo/search_form.html', {})

    if origin and destination and departureDate:
        try:
            flight_offers = amadeus.shopping.flight_offers_search.get(**kwargs)
            prediction_flights = amadeus.shopping.flight_offers.prediction.post(flight_offers.result)
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
            return render(request, 'demo/search_form.html', {})

        flights_offers_returned = []
        for flight in flight_offers.data:
            offer = Flight(flight).construct_flights()
            flights_offers_returned.append(offer)

        prediction_flights_returned = []
        for flight in prediction_flights.data:
            offer = Flight(flight).construct_flights()
            prediction_flights_returned.append(offer)
        return render(request, 'demo/search_results.html', {'response': flights_offers_returned,
                                                     'prediction': prediction_flights_returned,
                                                     'origin': origin,
                                                     'destination': destination,
                                                     'departureDate': departureDate,
                                                     'returnDate': returnDate,
                                                     'tripPurpose': tripPurpose,
                                                     })
    return render(request, 'demo/search_form.html', {})

def verify(request: HttpRequest) -> HttpResponse:
    if amadeus_status(request):
        return demo(request)
    else:
        return HttpResponseRedirect('../')

def amadeus_status(request: HttpRequest):
    if settings.CLIENT_ID in request.session and settings.CLIENT_SECRET in request.session:
        os.environ[settings.CLIENT_ID] = request.session[settings.CLIENT_ID]
        os.environ[settings.CLIENT_SECRET] = request.session[settings.CLIENT_SECRET]
        global amadeus
        amadeus = Client()
        return True
    return False