from django.urls import path

from . import views
from . import airports

urlpatterns = [
    path('', views.verify, name='verify'),
    path('origin_airport_search/', airports.verify, name='origin_airport_search'),
    path('destination_airport_search/', airports.verify, name='destination_airport_search'),
]
