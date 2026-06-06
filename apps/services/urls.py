from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('dich-vu/', views.service_list_view, name='service_list'),
    path('dich-vu/<int:service_id>/', views.service_detail_view, name='service_detail'),
]

