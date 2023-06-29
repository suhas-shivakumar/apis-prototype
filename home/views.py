from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.conf import settings
import os
import requests
from django.views.decorators.csrf import csrf_exempt


CLIENT_ID = "AMADEUS_CLIENT_ID"
CLIENT_SECRET = "AMADEUS_CLIENT_SECRET"

@csrf_exempt
def verify(request: HttpRequest) -> HttpResponse:
    client_id = request.POST.get("client_id", None)
    client_secret = request.POST.get("client_secret", None)
    # method = request.POST.get("method", None)
    if client_id is not None or client_secret is not None:
        os.environ[CLIENT_ID] = client_id
        os.environ[CLIENT_SECRET] = client_secret
        return render(request, 'home_page.html', {})
    
    return render(request, 'login.html', {})

@csrf_exempt
def chatgpt(request):
    message = request.GET.get("message", None)
    if message is None:
        message = request.POST.get("message", None)
    api_key = request.GET.get("session", None)
    if message:

        URL = "https://api.openai.com/v1/chat/completions"

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
