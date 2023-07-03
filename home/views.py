from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.conf import settings
import os
import requests




def verify(request: HttpRequest) -> HttpResponse:
    client_id = request.POST.get("client_id", None)
    client_secret = request.POST.get("client_secret", None)
    if settings.CLIENT_ID in request.session and settings.CLIENT_SECRET in request.session:
        return render(request, 'home_page.html', {})
    elif client_id is not None or client_secret is not None:
        request.session[settings.CLIENT_ID] = client_id
        request.session[settings.CLIENT_SECRET] = client_secret
        return render(request, 'home_page.html', {})
    
    return render(request, 'login.html', {})


def chatgpt(request):
    message = request.GET.get("message", None)
    if message is None:
        message = request.POST.get("message", None)
    api_key = request.GET.get("session", None)
    if message:

        URL = settings.OPEN_AI_URL

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": f"{message}"}],
            "temperature" : 1.0,
            "top_p":1.0,
            "n" : 1,
            "stream": False,
            "presence_penalty":0,
            "frequency_penalty":0,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        response = requests.post(URL, headers=headers, json=payload, stream=False, verify=False)
        return HttpResponse(response.json()["choices"][0]["message"]["content"])
    else:
        return render(request, 'chat.html', {})

def logout(request):
    id = request.session.pop(settings.CLIENT_ID)
    secret = request.session.pop(settings.CLIENT_SECRET)
    return render(request, 'login.html', {})