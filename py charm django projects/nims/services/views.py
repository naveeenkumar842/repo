from django.http import HttpResponse
from django.template import loader

from services.models import Service


# Create your views here.
def index(request):
    all_services = Service.objects.all()
    context = {
        'all_services':all_services

    }
    template = loader.get_template('services/index.html')
    return HttpResponse(template.render(context, request))



def serviceInfo(request, category_name):
    service = Service.objects.get(categeory=category_name)
    context = {
        'service': service
    }

    template = loader.get_template('services/services_info.html')

    return HttpResponse(template.render(context,request))