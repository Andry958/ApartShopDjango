from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Apartment
from .forms import ApartmentForm

FAVORITE_APARTMENTS_KEY = 'favorite_apartments'

def apartment_list(request):
    apartments = Apartment.objects.all()
    favorite_ids = request.session.get(FAVORITE_APARTMENTS_KEY, [])
    context = {
        'apartments': apartments,
        'total_apartments': apartments.count(),
        'available_apartments': apartments.filter(is_available=True).count(),
        'favorite_ids': favorite_ids,
    }
    return render(request, 'apartments/apartment_list.html', context)


def apartment_detail(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    favorite_ids = request.session.get(FAVORITE_APARTMENTS_KEY, [])
    is_favorite = pk in favorite_ids
    return render(request, 'apartments/apartment_detail.html', {
        'apartment': apartment,
        'is_favorite': is_favorite
    })

def apartment_create(request):
    if request.method == 'POST':
        form = ApartmentForm(request.POST)
        if form.is_valid():
            apartment = form.save()
            messages.success(request, f'Квартиру "{apartment.title}" успішно створено!')
            return redirect('apartment_detail', pk=apartment.pk)
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = ApartmentForm()
    
    return render(request, 'apartments/apartment_form.html', {
        'form': form,
        'title': 'Додати нову квартиру',
        'button_text': 'Створити'
    })

def apartment_update(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    if request.method == 'POST':
        form = ApartmentForm(request.POST, instance=apartment)
        if form.is_valid():
            apartment = form.save()
            messages.success(request, f'Квартиру "{apartment.title}" успішно оновлено!')
            return redirect('apartment_detail', pk=apartment.pk)
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = ApartmentForm(instance=apartment)
    
    return render(request, 'apartments/apartment_form.html', {
        'form': form,
        'title': f'Редагувати: {apartment.title}',
        'button_text': 'Зберегти зміни',
        'apartment': apartment
    })

def apartment_delete(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    if request.method == 'POST':
        title = apartment.title
        apartment.delete()
        messages.success(request, f'Квартиру "{title}" успішно видалено!')
        return redirect('apartment_list')
    
    return render(request, 'apartments/apartment_confirm_delete.html', {
        'apartment': apartment
    })


def add_to_favorites(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    favorite_ids = request.session.get(FAVORITE_APARTMENTS_KEY, [])
    
    if pk not in favorite_ids:
        favorite_ids.append(pk)
        request.session[FAVORITE_APARTMENTS_KEY] = favorite_ids
        messages.success(request, f'Квартиру "{apartment.title}" додано до улюблених!')
    
    return redirect(request.META.get('HTTP_REFERER', 'apartment_list'))


def remove_from_favorites(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    favorite_ids = request.session.get(FAVORITE_APARTMENTS_KEY, [])
    
    if pk in favorite_ids:
        favorite_ids.remove(pk)
        request.session[FAVORITE_APARTMENTS_KEY] = favorite_ids
        messages.success(request, f'Квартиру "{apartment.title}" видалено з улюблених!')
    
    return redirect(request.META.get('HTTP_REFERER', 'apartment_list'))


def favorites_list(request):
    favorite_ids = request.session.get(FAVORITE_APARTMENTS_KEY, [])
    apartments = Apartment.objects.filter(pk__in=favorite_ids)
    
    context = {
        'apartments': apartments,
        'favorite_ids': favorite_ids,
    }
    return render(request, 'apartments/favorites_list.html', context)
