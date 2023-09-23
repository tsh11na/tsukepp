from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render

from .models import Tsuke
from .forms import TsukeCreateForm

class IndexView(generic.TemplateView):
    """トップページ"""
    template_name = "tsuke/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
    
        if self.request.user.is_authenticated:
            context["user"] = self.request.user
        else:
            context["user"] = None
        return context


class TsukeHistoryView(LoginRequiredMixin, generic.ListView):  # TODO: LoginRequiredMixin
    """ツケ履歴"""
    model = Tsuke
    template_name = 'tsuke/history.html'

    def get_queryset(self) -> QuerySet[Any]:
        return Tsuke.objects.filter(user=self.request.user).order_by("-purchase_datetime")


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


def tsuke_pay(request):
    return render(request, "tsuke/pay.html")
