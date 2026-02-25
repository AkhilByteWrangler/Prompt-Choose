from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
import os

def health_check(request):
    """Health check endpoint to verify environment variables"""
    return JsonResponse({
        'status': 'ok',
        'env_vars': {
            'MONGODB_URI_exists': bool(os.environ.get('MONGODB_URI')),
            'MONGODB_NAME': os.environ.get('MONGODB_NAME', 'NOT SET'),
            'OPENAI_API_KEY_exists': bool(os.environ.get('OPENAI_API_KEY')),
            'SECRET_KEY_exists': bool(os.environ.get('SECRET_KEY')),
            'DEBUG': os.environ.get('DEBUG', 'False'),
            'PORT': os.environ.get('PORT', 'NOT SET'),
        },
        'settings': {
            'DEBUG': settings.DEBUG,
            'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('health/', health_check, name='health'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
