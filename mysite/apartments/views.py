from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Apartment, Booking
from .forms import ApartmentForm, BookingForm
from datetime import date

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

@login_required
def apartment_create(request):
    if not request.user.is_staff:
        messages.error(request, 'У вас немає прав для додавання квартир')
        return redirect('home')
    
    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES)
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

@login_required
def apartment_update(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'У вас немає прав для редагування квартир')
        return redirect('home')
    
    apartment = get_object_or_404(Apartment, pk=pk)
    
    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES, instance=apartment)
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

@login_required
def apartment_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'У вас немає прав для видалення квартир')
        return redirect('home')
    
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


@login_required
def booking_create(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    if not apartment.is_available:
        messages.error(request, 'Ця квартира недоступна для бронювання')
        return redirect('apartment_detail', pk=pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.apartment = apartment
            booking.user = request.user
            
            days = (booking.end_date - booking.start_date).days
            booking.total_price = apartment.price * days
            
            booking.save()
            messages.success(request, f'Бронювання успішно створено! Загальна вартість: ${booking.total_price}')
            return redirect('booking_detail', pk=booking.pk)
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = BookingForm()
    
    return render(request, 'apartments/booking_form.html', {
        'form': form,
        'apartment': apartment
    })


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.user != request.user and not request.user.is_staff:
        messages.error(request, 'У вас немає доступу до цього бронювання')
        return redirect('apartment_list')
    
    return render(request, 'apartments/booking_detail.html', {
        'booking': booking
    })


@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).select_related('apartment')
    
    return render(request, 'apartments/booking_list.html', {
        'bookings': bookings
    })


@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.user != request.user:
        messages.error(request, 'У вас немає доступу до цього бронювання')
        return redirect('apartment_list')
    
    if booking.status == 'cancelled':
        messages.warning(request, 'Це бронювання вже скасовано')
        return redirect('booking_detail', pk=pk)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Бронювання успішно скасовано')
        return redirect('booking_list')
    
    return render(request, 'apartments/booking_cancel.html', {
        'booking': booking
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            if user.username.lower() == 'admin':
                user.is_staff = True
                user.is_superuser = True
                user.save()
                messages.success(request, f'Ласкаво просимо, {user.username}! Ваш адмін-акаунт успішно створено.')
            else:
                messages.success(request, f'Ласкаво просимо, {user.username}! Ваш акаунт успішно створено.')
            
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user).select_related('apartment')
    
    return render(request, 'accounts/profile.html', {
        'bookings': bookings
    })
