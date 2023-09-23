from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Tsuke
from .forms import TsukeCreateForm

class IndexView(generic.TemplateView):
    """トップページ"""
    template_name = "tsuke/index.html"


class TsukeHistoryView(LoginRequiredMixin, generic.ListView):  # TODO: LoginRequiredMixin
    """ツケ履歴"""
    model = Tsuke
    template_name = 'tsuke/history.html'


class TsukeCreateView(LoginRequiredMixin, generic.CreateView):
    """ツケの登録"""
    model = Tsuke
    template_name = "tsuke/create.html"
    form_class = TsukeCreateForm
    success_url = reverse_lazy("tsuke:index")

    def form_valid(self, form):
        tsuke = form.save(commit=False)
        tsuke.user = self.request.user
        tsuke.save()
        messages.success(self.request, "ツケを登録しました。")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "ツケの登録に失敗しました。")
        return super().form_invalid(form)
