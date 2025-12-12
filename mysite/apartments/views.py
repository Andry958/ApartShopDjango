from django.shortcuts import render, get_object_or_404, redirect
from .models import Apartment

# Список всіх квартир
def apartment_list(request):
    apartments = Apartment.objects.all()
    return render(request, 'apartments/apartment_list.html', {'apartments': apartments})

# Деталі однієї квартири
def apartment_detail(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    return render(request, 'apartments/apartment_detail.html', {'apartment': apartment})

# Видалити квартиру (якщо потрібно)
def apartment_delete(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    apartment.delete()
    return redirect('apartment_list')
