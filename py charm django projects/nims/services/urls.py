from django.urls import path
from.import views

app_name = 'services'

urlpatterns =[
    path('', views.index, name='index'),
    path('services/',views.serviceInfo,name='service_info'),
    path('(?P<category_name>[^%s]*)/',views.serviceInfo,name='service_info')
]