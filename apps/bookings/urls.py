from django.urls import path
from . import views

urlpatterns = [
    path('dat-lich/<int:service_id>/', views.booking_create_view, name='booking_create'),
    path('thanh-toan-thanh-cong/<int:booking_id>/', views.payment_success_view, name='payment_success'),
    path('tra-cuu/', views.search_order_view, name='search_order'),
]