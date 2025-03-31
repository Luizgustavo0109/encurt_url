from django.urls import path
from encurtador_urls import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('valida_url/', views.valida_url, name='valida_url'),
    path('<str:url>/', views.redirecionar, name='redirecionar'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)