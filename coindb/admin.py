from django.contrib import admin
from .models import Coin, Country, Collector, Shop, Material

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "continent")
    search_fields = ("name", "code")

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'price', 'country', 'shop')
    search_fields = ('name', 'country__name', 'shop__name')
    list_filter = ("year", "country")

@admin.register(Collector)
class CollectorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")
    search_fields = ("first_name", "last_name", "email")

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "contact_info")
    search_fields = ("name",)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)

