from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import TsukeCreateForm, TsukePayConfirmForm, TsukePaySelectForm
from .models import Tsuke
from .security import is_valid_token, set_submit_token


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
    form = TsukePaySelectForm(user=request.user)
    tsuke_list = form.fields['tsuke_list'].queryset.order_by("-purchase_date")

    return render(request, "tsuke/pay_select.html", {"tsuke_list": tsuke_list})

@login_required
def tsuke_pay_confirm(request):
    """清算確認画面"""
    selected_ids = request.POST.getlist("tsuke_list")

    # 確認画面
    form = TsukePayConfirmForm(request.POST, tsuke_ids=selected_ids)
    tsuke_list = form.fields['tsuke_list'].queryset

    if not form.is_valid():
         return render(request, "tsuke/pay_select.html", {"tsuke_list": tsuke_list, "form": form})

    return render(request, "tsuke/pay_confirm.html", {"tsuke_list": tsuke_list})

@login_required
def settle(request):
    """決済処理"""

    if request.method == "POST":
        try: # 更新処理
            # 決済対象のツケを取得
            selected_ids = request.POST.getlist("tsuke_list")
            checking_tsuke_list = Tsuke.objects.filter(id__in=selected_ids)

            # 清算済に変更
            for tsuke in checking_tsuke_list:
                tsuke.is_paid = True

            Tsuke.objects.bulk_update(checking_tsuke_list, fields=["is_paid"])

        except(KeyError, Tsuke.DoesNotExist):
            pass  # TODO エラー処理

        else:  # 成功時
            return HttpResponseRedirect(reverse_lazy("tsuke:index"))

    else:  # 決済処理はPOSTからしか呼び出せない
        return HttpResponseNotAllowed(["POST"])
