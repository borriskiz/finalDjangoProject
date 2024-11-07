from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from coindb.models import Coin, Country, Shop
from coindb.filters import CoinFilterSet, ShopFilterSet, CountryFilterSet


class CoinListView(ListView):
    model = Coin
    template_name = 'coin/coin_list.html'
    context_object_name = 'coins'
    filterset_class = CoinFilterSet
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        coin_filter = CoinFilterSet(self.request.GET, queryset=queryset)
        queryset = coin_filter.qs

        sort_field = self.request.GET.get('sort', 'name')
        order = self.request.GET.get('order', 'asc')
        if order == 'desc':
            sort_field = f'-{sort_field}'

        queryset = queryset.order_by(sort_field)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['filter'] = CoinFilterSet(self.request.GET, queryset=queryset)
        return context


class CoinDetailView(DetailView):
    model = Coin
    template_name = 'coin/coin_detail.html'
    context_object_name = 'coin'


class CoinCreateView(CreateView):
    model = Coin
    template_name = 'coin/coin_form.html'
    fields = ['name', 'year', 'country', 'material', 'price', 'imageObverse', 'imageReverse',
              'shop']

    def get_success_url(self):
        return reverse_lazy('coin_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Можно дополнительно передать данные, если нужно
        context['countries'] = Country.objects.all()
        context['shops'] = Shop.objects.all()
        return context


class CoinUpdateView(UpdateView):
    model = Coin
    template_name = 'coin/coin_form.html'
    fields = ['name', 'year', 'country', 'material', 'price', 'imageObverse', 'imageReverse', ]
    success_url = reverse_lazy('coin_list')


class CoinDeleteView(DeleteView):
    model = Coin
    template_name = 'coin/coin_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('coin_list')


class CountryListView(ListView):
    model = Country
    template_name = 'country/country_list.html'
    context_object_name = 'countries'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        country_filter = CountryFilterSet(self.request.GET, queryset=queryset)
        filtered_queryset = country_filter.qs

        sort = self.request.GET.get('sort', 'name')
        order = self.request.GET.get('order', 'asc')
        if order == 'desc':
            sort = f'-{sort}'

        return filtered_queryset.order_by(sort)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()

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
    fields = ['name', 'continent', 'code']

    def get_success_url(self):
        return reverse_lazy('country_detail',
                            kwargs={'pk': self.object.pk})


class CountryUpdateView(UpdateView):
    model = Country
    template_name = 'country/country_form.html'
    fields = ['name', 'continent', 'code']
    success_url = reverse_lazy('country_list')


class CountryDeleteView(DeleteView):
    model = Country
    template_name = 'country/country_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('country_list')


class ShopListView(ListView):
    model = Shop
    template_name = 'shop/shop_list.html'
    context_object_name = 'shops'
    filterset_class = ShopFilterSet
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        shop_filter = ShopFilterSet(self.request.GET, queryset=queryset)
        queryset = shop_filter.qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['filter'] = ShopFilterSet(self.request.GET, queryset=queryset)
        return context


class ShopDetailView(DetailView):
    model = Shop
    template_name = 'shop/shop_detail.html'
    context_object_name = 'shop'


class ShopCreateView(CreateView):
    model = Shop
    template_name = 'shop/shop_form.html'
    fields = ['name', 'location', 'contact_info']

    def get_success_url(self):
        return reverse_lazy('shop_detail', kwargs={'pk': self.object.pk})


class ShopUpdateView(UpdateView):
    model = Shop
    template_name = 'shop/shop_form.html'
    fields = ['name', 'location', 'contact_info']
    success_url = reverse_lazy('shop_list')


class ShopDeleteView(DeleteView):
    model = Shop
    template_name = 'shop/shop_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('shop_list')
