from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.apartment_list, name='apartment_list'),
    path('create/', views.apartment_create, name='apartment_create'),
    path('<int:pk>/', views.apartment_detail, name='apartment_detail'),
    path('<int:pk>/update/', views.apartment_update, name='apartment_update'),
    path('<int:pk>/delete/', views.apartment_delete, name='apartment_delete'),
    path('<int:pk>/add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('<int:pk>/remove-from-favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('<int:pk>/book/', views.booking_create, name='booking_create'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:pk>/cancel/', views.booking_cancel, name='booking_cancel'),
]
