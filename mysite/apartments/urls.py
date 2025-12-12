from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.apartment_list, name='apartment_list'), 
    path('<int:pk>/', views.apartment_detail, name='apartment_detail'),  
    path('delete/<int:pk>/', views.apartment_delete, name='apartment_delete'), 
]
