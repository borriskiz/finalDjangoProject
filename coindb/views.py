from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from coindb.models import Coin, Country, Shop
from coindb.filters import CoinFilterSet, ShopFilterSet, CountryFilterSet  # если ты хочешь использовать фильтрацию


# Список монет
class CoinListView(ListView):
    model = Coin
    template_name = 'coin/coin_list.html'
    context_object_name = 'coins'
    paginate_by = 10
    filterset_class = CoinFilterSet

    def get_queryset(self):
        # Получаем фильтрованный queryset
        queryset = super().get_queryset()

        # Применяем фильтр
        coin_filter = CoinFilterSet(self.request.GET, queryset=queryset)
        queryset = coin_filter.qs

        # Обработка сортировки
        sort_field = self.request.GET.get('sort', 'name')  # Поле по умолчанию
        order = self.request.GET.get('order', 'asc')  # Порядок сортировки по умолчанию
        if order == 'desc':
            sort_field = f'-{sort_field}'  # Для убывающей сортировки добавляем минус

        # Применяем сортировку
        return queryset.order_by(sort_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CoinFilterSet(self.request.GET, queryset=self.get_queryset())
        return context


class CoinDetailView(DetailView):
    model = Coin
    template_name = 'coin/coin_detail.html'
    context_object_name = 'coin'


# Создание новой монеты
class CoinCreateView(CreateView):
    model = Coin
    template_name = 'coin/coin_form.html'
    fields = ['name', 'year', 'country', 'material', 'price', 'image', 'shop']  # Укажи поля для формы

    def get_success_url(self):
        return reverse_lazy('coin_detail', kwargs={'pk': self.object.pk})  # Перенаправление после успешного сохранения

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Можно дополнительно передать данные, если нужно
        context['countries'] = Country.objects.all()
        context['shops'] = Shop.objects.all()
        return context


# Обновление монеты
class CoinUpdateView(UpdateView):
    model = Coin
    template_name = 'coin/coin_form.html'
    fields = ['name', 'year', 'country', 'material', 'price', 'image']  # Поля для обновления
    success_url = reverse_lazy('coin_list')  # Перенаправление после успешного обновления


# Удаление монеты
class CoinDeleteView(DeleteView):
    model = Coin
    template_name = 'coin/coin_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('coin_list')  # Перенаправление на список монет после удаления


class CountryListView(ListView):
    model = Country
    template_name = 'country/country_list.html'
    context_object_name = 'countries'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Применяем фильтр
        country_filter = CountryFilterSet(self.request.GET, queryset=queryset)
        filtered_queryset = country_filter.qs

        # Сортировка
        sort = self.request.GET.get('sort', 'name')
        order = self.request.GET.get('order', 'asc')
        if order == 'desc':
            sort = f'-{sort}'

        # Возвращаем отфильтрованный и отсортированный queryset
        return filtered_queryset.order_by(sort)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем отфильтрованный и отсортированный queryset
        queryset = self.get_queryset()

        # Пагинация
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['filter'] = CountryFilterSet(self.request.GET, queryset=queryset)

        return context

class CountryDetailView(DetailView):
    model = Country
    template_name = 'country/country_detail.html'
    context_object_name = 'country'


class CountryCreateView(CreateView):
    model = Country
    template_name = 'country/country_form.html'
    fields = ['name', 'continent', 'code']  # Указываем поля для формы

    def get_success_url(self):
        return reverse_lazy('country_detail',
                            kwargs={'pk': self.object.pk})  # Перенаправление после успешного сохранения


class CountryUpdateView(UpdateView):
    model = Country
    template_name = 'country/country_form.html'
    fields = ['name', 'continent', 'code']  # Поля для обновления
    success_url = reverse_lazy('country_list')  # Перенаправление после успешного обновления


class CountryDeleteView(DeleteView):
    model = Country
    template_name = 'country/country_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('country_list')  # Перенаправление на список стран после удаления


class ShopListView(ListView):
    model = Shop
    template_name = 'shop/shop_list.html'
    context_object_name = 'shops'
    paginate_by = 10
    filterset_class = ShopFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()

        # Применяем фильтр, если есть параметры GET
        shop_filter = ShopFilterSet(self.request.GET, queryset=queryset)
        queryset = shop_filter.qs

        # Сортировка по столбцам
        sort_field = self.request.GET.get('sort', 'name')  # Поле по умолчанию
        order = self.request.GET.get('order', 'asc')  # Порядок сортировки по умолчанию
        if order == 'desc':
            sort_field = f'-{sort_field}'  # Для убывающей сортировки добавляем минус

        return queryset.order_by(sort_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ShopFilterSet(self.request.GET, queryset=self.get_queryset())
        return context


class ShopDetailView(DetailView):
    model = Shop
    template_name = 'shop/shop_detail.html'
    context_object_name = 'shop'


class ShopCreateView(CreateView):
    model = Shop
    template_name = 'shop/shop_form.html'
    fields = ['name', 'location', 'contact_info']  # Указываем поля для формы

    def get_success_url(self):
        return reverse_lazy('shop_detail', kwargs={'pk': self.object.pk})  # Перенаправление после успешного сохранения


class ShopUpdateView(UpdateView):
    model = Shop
    template_name = 'shop/shop_form.html'
    fields = ['name', 'location', 'contact_info']  # Поля для обновления
    success_url = reverse_lazy('shop_list')  # Перенаправление после успешного обновления


class ShopDeleteView(DeleteView):
    model = Shop
    template_name = 'shop/shop_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('shop_list')  # Перенаправление на список магазинов после удаления
