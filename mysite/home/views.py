from django.shortcuts import render
from apartments.models import Apartment


def home(request):
    apartments = Apartment.objects.all().order_by('-created_at')
    favorite_ids = request.session.get('favorite_apartments', [])
    context = {
        'apartments': apartments,
        'favorite_ids': favorite_ids,
    }
    return render(request, "Home/index.html", context)