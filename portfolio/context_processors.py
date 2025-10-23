from django.conf import settings

def analytics(request):
    return {
        'GA_MEASUREMENT_ID': getattr(settings, 'GA_MEASUREMENT_ID', None),
        'CALENDLY_URL': getattr(settings, 'CALENDLY_URL', ''),
    }
