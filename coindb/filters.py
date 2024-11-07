import django_filters
from django.db.models import Q
from .models import Coin, Country, Material

class CoinFilterSet(django_filters.FilterSet):
    price_range = django_filters.RangeFilter(field_name='price', label='Цена от и до')
    year_range = django_filters.RangeFilter(field_name='year', label='Год выпуска от и до')
    country = django_filters.ModelChoiceFilter(queryset=Country.objects.all(), field_name='country', label='Страна')
    material = django_filters.ModelMultipleChoiceFilter(queryset=Material.objects.all(), field_name='material', label='Материал')
    term = django_filters.CharFilter(method='filter_term', label='Поиск')

    class Meta:
        model = Coin
        fields = ['term', 'price_range', 'year_range', 'country', 'material']

    def filter_term(self, queryset, name, value):
        if value:
            criteria = Q()
            for term in value.split():
                criteria |= Q(name__icontains=term) | Q(country__name__icontains=term) | Q(material__name__icontains=term)
            return queryset.filter(criteria).distinct()
        return queryset
