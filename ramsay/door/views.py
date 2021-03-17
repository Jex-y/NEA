from django.shortcuts import render
from django.views.generic import TemplateView
from ramsay import settings

def MainView(request):
    """
    Renders the door view

    Meets requirements: 3.01, 3.02, 3.04, 3.04, 3.05
    
    Parameters:
        request (HttpRequest): The request that called the view

    Returns:
        (HttpResponse): Webpage showing incomplete item orders
    """
    return render(request, 'door/index.html', {
        "settings":settings
        })

