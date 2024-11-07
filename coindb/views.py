
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from coindb.models import Coin, Country, Shop
from coindb.filters import CoinFilterSet  # если ты хочешь использовать фильтрацию

# Список монет
class CoinListView(ListView):
    model = Coin
    template_name = 'coin/coin_list.html'
    context_object_name = 'coins'
    filterset_class = CoinFilterSet
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.coin_filter = CoinFilterSet(self.request.GET, queryset=queryset)
        return self.coin_filter.qs  # Возвращаем отфильтрованный queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.coin_filter  # Передаем фильтр в контекст
        return context
# Детали монеты
class CoinDetailView(DetailView):
    model = Coin
    template_name = 'coin/coin_detail.html'
    context_object_name = 'coin'

# Создание новой монеты
class CoinCreateView(CreateView):
    model = Coin
    template_name = 'coin/coin_form.html'
    fields = ['name', 'year', 'country', 'material', 'price', 'image','shop']  # Укажи поля для формы

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

