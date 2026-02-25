from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
import os

def serve_spa(request, path=''):
    """Serve the SPA for all non-API routes"""
    index_path = os.path.join(settings.STATIC_ROOT, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'rb') as f:
            from django.http import HttpResponse
            return HttpResponse(f.read(), content_type='text/html')
    from django.http import HttpResponseNotFound
    return HttpResponseNotFound('Frontend not built')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    re_path(r'^.*$', serve_spa, name='spa'),
]
