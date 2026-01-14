FAVORITE_APARTMENTS_KEY = 'favorite_apartments'


def favorites_context(request):
    favorite_ids = request.session.get(FAVORITE_APARTMENTS_KEY, [])
    return {
        'favorites_count': len(favorite_ids),
        'favorite_ids': favorite_ids,
    }
