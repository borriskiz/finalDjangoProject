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
                  path('countries/', views.CountryListView.as_view(), name='country_list'),

                  path('countries/<int:pk>/', views.CountryDetailView.as_view(), name='country_detail'),
                  path('countries/create/', views.CountryCreateView.as_view(), name='country_create'),
                  path('countries/<int:pk>/edit/', views.CountryUpdateView.as_view(), name='country_update'),
                  path('countries/<int:pk>/delete/', views.CountryDeleteView.as_view(), name='country_delete'),

                  path('shops/', views.ShopListView.as_view(), name='shop_list'),
                  path('shops/<int:pk>/', views.ShopDetailView.as_view(), name='shop_detail'),
                  path('shops/create/', views.ShopCreateView.as_view(), name='shop_create'),
                  path('shops/<int:pk>/edit/', views.ShopUpdateView.as_view(), name='shop_update'),
                  path('shops/<int:pk>/delete/', views.ShopDeleteView.as_view(), name='shop_delete'),

                  path('material/', views.MaterialListView.as_view(), name='material_list'),
                  path('material/<int:pk>/', views.MaterialDetailView.as_view(), name='material_detail'),
                  path('material/create/', views.MaterialCreateView.as_view(), name='material_create'),
                  path('material/<int:pk>/edit/', views.MaterialUpdateView.as_view(), name='material_update'),
                  path('material/<int:pk>/delete/', views.MaterialDeleteView.as_view(), name='material_delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
