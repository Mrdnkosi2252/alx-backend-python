from django.urls import path, include





from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')