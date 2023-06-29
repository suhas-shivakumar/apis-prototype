from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.verify, name='verify'),
    path('snd_msg_to_bot/', views.chatgpt, name='chatbot'),
    path('flight_search/', include('flight_search.urls')),
    path('trip_purpose/', include('trip_purpose.urls')),
]
