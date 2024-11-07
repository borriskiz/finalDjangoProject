from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from coindb.models import Coin, Country, Shop, Material, CoinCollection
from coindb.filters import CoinFilterSet, ShopFilterSet, CountryFilterSet, MaterialFilterSet
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        coins = Coin.objects.filter(coincollection__user=request.user)
        coin_filter = CoinFilterSet(request.GET, queryset=coins)
        coins = coin_filter.qs

        sort_field = request.GET.get('sort', 'name')
        order = request.GET.get('order', 'asc')
        if order == 'desc':
            sort_field = f'-{sort_field}'
        coins = coins.order_by(sort_field)

        paginator = Paginator(coins, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'profile.html', {
            'page_obj': page_obj,
            'filter': coin_filter,
        })


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


class CoinDetailView(LoginRequiredMixin, DetailView):
    model = Coin
    template_name = 'coin/coin_detail.html'
    context_object_name = 'coin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coin = self.object
        # Проверяем, авторизован ли пользователь
        if self.request.user.is_authenticated:
            is_in_collection = CoinCollection.objects.filter(user=self.request.user, coin=coin).exists()
            context['is_in_collection'] = is_in_collection
        else:
            context['is_in_collection'] = False
        return context


class CoinCreateView(LoginRequiredMixin, CreateView):
    model = Coin
    template_name = 'coin/coin_form.html'
    fields = ['name', 'year', 'country', 'material', 'price', 'imageObverse', 'imageReverse',
              'shop']

    def get_success_url(self):
        return reverse_lazy('coin_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['shops'] = Shop.objects.all()
        return context


class CoinUpdateView(LoginRequiredMixin, UpdateView):
    model = Coin
    template_name = 'coin/coin_form.html'
    fields = ['name', 'year', 'country', 'material', 'price', 'imageObverse', 'imageReverse', ]
    success_url = reverse_lazy('coin_list')


class CoinDeleteView(LoginRequiredMixin, DeleteView):
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


class CountryDetailView(LoginRequiredMixin, DetailView):
    model = Country
    template_name = 'country/country_detail.html'
    context_object_name = 'country'


class CountryCreateView(LoginRequiredMixin, CreateView):
    model = Country
    template_name = 'country/country_form.html'
    fields = ['name', 'continent', 'code']

    def get_success_url(self):
        return reverse_lazy('country_detail',
                            kwargs={'pk': self.object.pk})


class CountryUpdateView(LoginRequiredMixin, UpdateView):
    model = Country
    template_name = 'country/country_form.html'
    fields = ['name', 'continent', 'code']
    success_url = reverse_lazy('country_list')


class CountryDeleteView(LoginRequiredMixin, DeleteView):
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


class ShopDetailView(LoginRequiredMixin, DetailView):
    model = Shop
    template_name = 'shop/shop_detail.html'
    context_object_name = 'shop'


class ShopCreateView(LoginRequiredMixin, CreateView):
    model = Shop
    template_name = 'shop/shop_form.html'
    fields = ['name', 'location', 'contact_info']

    def get_success_url(self):
        return reverse_lazy('shop_detail', kwargs={'pk': self.object.pk})


class ShopUpdateView(LoginRequiredMixin, UpdateView):
    model = Shop
    template_name = 'shop/shop_form.html'
    fields = ['name', 'location', 'contact_info']
    success_url = reverse_lazy('shop_list')


class ShopDeleteView(LoginRequiredMixin, DeleteView):
    model = Shop
    template_name = 'shop/shop_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('shop_list')


class MaterialListView(ListView):
    model = Material
    template_name = 'material/material_list.html'
    context_object_name = 'materials'
    filterset_class = MaterialFilterSet
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        material_filter = MaterialFilterSet(self.request.GET, queryset=queryset)
        queryset = material_filter.qs

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
        context['filter'] = MaterialFilterSet(self.request.GET, queryset=queryset)
        return context


class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = Material
    template_name = 'material/material_detail.html'
    context_object_name = 'material'


class MaterialCreateView(LoginRequiredMixin, CreateView):
    model = Material
    template_name = 'material/material_form.html'
    fields = ['name', 'price']

    def get_success_url(self):
        return reverse_lazy('material_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MaterialUpdateView(LoginRequiredMixin, UpdateView):
    model = Material
    template_name = 'material/material_form.html'
    fields = ['name', 'price']
    success_url = reverse_lazy('material_list')


class MaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = Material
    template_name = 'material/material_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('material_list')


class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('coin_list')
        return render(request, 'registration/signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('coin_list')
        return render(request, 'registration/login.html', {'form': form})


class ToggleCollectionView(LoginRequiredMixin, View):
    def get(self, request, coin_id):
        coin = get_object_or_404(Coin, pk=coin_id)

        coin_collection = CoinCollection.objects.filter(user=request.user, coin=coin)

        if coin_collection.exists():
            coin_collection.delete()
        else:
            CoinCollection.objects.create(user=request.user, coin=coin)

        return redirect('coin_detail', pk=coin.pk)
