from django.http import JsonResponse
from django.shortcuts import redirect


def home(request):
    return redirect("feed")


def health(request):
    return JsonResponse({"status": "ok"})
