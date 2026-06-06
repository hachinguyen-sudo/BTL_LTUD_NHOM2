from django.shortcuts import render, get_object_or_404
from .models import Service

def home_view(request):
    services = Service.objects.filter(is_active=True).order_by('-created_at')[:3]
    return render(request, 'services/home.html', {'services': services})

def service_list_view(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'services/services.html', {'services': services})


def service_detail_view(request, service_id):
    service = get_object_or_404(Service, id=service_id, is_active=True)
    return render(request, 'services/services-detail.html', {'service': service})