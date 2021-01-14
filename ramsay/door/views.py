from django.shortcuts import render
from django.views.generic import TemplateView
from ramsay import settings

def MainView(request):
    return render(request, 'door/index.html', {
        "settings":settings
        })

