from django.conf import settings


def site(request):
    """Makes {{ SITE_NAME }} available in every template."""
    return {"SITE_NAME": settings.SITE_NAME}