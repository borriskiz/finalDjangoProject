"""
URL configuration for finalDjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from coindb import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.CoinListView.as_view(), name='coin_list'),

                  path('coin/<int:pk>/', views.CoinDetailView.as_view(), name='coin_detail'),
                  path('coin/new/', views.CoinCreateView.as_view(), name='coin_create'),
                  path('coin/<int:pk>/edit/', views.CoinUpdateView.as_view(), name='coin_edit'),
                  path('coin/<int:pk>/delete/', views.CoinDeleteView.as_view(), name='coin_delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
