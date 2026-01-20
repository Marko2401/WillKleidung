from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('market.urls')),
]

# WICHTIG: Diese Zeilen hinzufügen!
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root='static')