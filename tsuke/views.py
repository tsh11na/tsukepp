from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import TsukeCreateForm, TsukePaySelectForm
from .models import Tsuke
from .security import is_valid_token, set_submit_token
from .utils import settle


class IndexView(generic.TemplateView):
    """トップページ"""
    template_name = "tsuke/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        unpaid_tsuke_list = Tsuke.objects.filter(user=self.request.user.id, is_paid=False)

        context["unpaid_amount"] = unpaid_tsuke_list.aggregate(Sum("amount"))
        context["unpaid_count"] = len(unpaid_tsuke_list)

        if self.request.user.is_authenticated:
            context["user"] = self.request.user
        else:
            context["user"] = None
        return context


class TsukeHistoryView(LoginRequiredMixin, generic.ListView):
    """ツケ履歴"""
    model = Tsuke
    template_name = 'tsuke/history.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return Tsuke.objects.filter(user=self.request.user).order_by("-purchase_date")


class TsukeCreateView(LoginRequiredMixin, generic.CreateView):
    """ツケの登録"""
    model = Tsuke
    template_name = "tsuke/create.html"
    form_class = TsukeCreateForm
    success_url = reverse_lazy("tsuke:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_token'] = set_submit_token(self.request)
        return context

    # https://omkz.net/djagno-parameter-modelform/
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        if is_valid_token(self.request):
            tsuke = form.save(commit=False)
            tsuke.user = self.request.user
            tsuke.save()
            return super().form_valid(form)
        else:
            return redirect("tsuke:index")

    def form_invalid(self, form):
        return super().form_invalid(form)

@login_required
def tsuke_pay_select(request):
    """清算選択画面"""

    if request.method == "POST":
        form = TsukePaySelectForm(request.POST, user=request.user)
        if form.is_valid():
            selected_tsukes = form.cleaned_data["unpaid_tsukes"]
            request.session["selected_ids"] = (
                [t.id for t in selected_tsukes]
            )
            return redirect("tsuke:pay_confirm")
        
        else:
            return render(request, "tsuke/pay_select.html", {"form": form})
    
    # GET
    form = TsukePaySelectForm(user=request.user)
    return render(request, "tsuke/pay_select.html", {"form": form})


class TsukePayConfirmView(LoginRequiredMixin, generic.ListView):
    """清算確認画面"""
    model = Tsuke
    template_name = 'tsuke/pay_confirm.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_token'] = set_submit_token(self.request)
        return context

    def get_queryset(self) -> QuerySet[Any]:
        selected_ids = self.request.session.get("selected_ids", [])
        return Tsuke.objects.filter(user=self.request.user, id__in=selected_ids).order_by("-purchase_date")

    def post(self, request):
        selected_ids = self.request.session.get("selected_ids", [])

        # 決済処理
        result = settle(selected_ids)
        request.session.pop("selected_ids", None)

        if result:
            # TODO 決済成功のメッセージ
            return redirect("tsuke:index")
        else:
            # TODO 決済失敗のメッセージ
            return redirect("tsuke:index")

