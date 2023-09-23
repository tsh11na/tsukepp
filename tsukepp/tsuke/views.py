from typing import Any
from django.db.models import Sum, Count
from django.db.models.query import QuerySet
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect


from .models import Tsuke
from .forms import TsukeCreateForm, TsukePaySelectForm, TsukePayConfirmForm


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

def tsuke_pay_select(request):
    """支払い選択画面"""
    unpaid_tsuke_list = Tsuke.objects.filter(user=request.user, is_paid=False)

    form = TsukePaySelectForm()
    form.fields['selected_ids'].queryset = unpaid_tsuke_list
    
    return render(request, "tsuke/pay_select.html", {"form": form})

def tsuke_pay_confirm(request):
    """支払い確認画面"""

    selected_ids = request.POST.getlist("selected_ids")
    checking_tsuke_list = Tsuke.objects.filter(id__in=selected_ids)

    # 「支払う」ボタン押下時：決済処理
    if request.method == "POST" and request.POST["page"] == "confirm":
        form = TsukePayConfirmForm(request.POST)
        form.fields["selected_ids"].queryset = checking_tsuke_list

        if form.is_valid():
            return redirect('tsuke:settle')

    # 確認画面
    form = TsukePayConfirmForm(request.POST)
    form.fields["selected_ids"].queryset = checking_tsuke_list
    return render(request, "tsuke/pay_confirm.html", {"form": form})

def settle(request):
    """決済処理"""

    try: # 更新処理
        # 決済対象のツケを取得
        selected_ids = request.POST.getlist("selected_ids")
        checking_tsuke_list = Tsuke.objects.filter(id__in=selected_ids)

        # 支払済に変更
        for tsuke in checking_tsuke_list:
            tsuke.is_paid = True

        Tsuke.objects.bulk_update(checking_tsuke_list, fields=["is_paid"])

    except(KeyError, Tsuke.DoesNotExist):
        pass  # TODO エラー処理

    else:  # 成功時
        return HttpResponseRedirect(reverse_lazy("tsuke:index"))

# class TsukePayConfirmView(LoginRequiredMixin, generic.FormView):
#     template_name = "tsuke/pay_confirm.html"
#     form_class = TsukePayConfirmForm
#     success_url = reverse_lazy("tsuke:index")

#     def get_form(self, form_class=None):

#         selected_ids = self.request.POST.getlist("selected_ids")
#         checking_tsuke_list = Tsuke.objects.filter(id__in=selected_ids)

#         # フォームを取得し、選択されたツケのリストをセット
#         form = super().get_form(form_class)
#         form.fields["tsuke_list"].queryset = checking_tsuke_list
#         return form

#     def form_valid(self, form):
#         pass
#         # 選択されたIDに対する一括更新処理を実行
#         # 例: YourModel.objects.filter(id__in=selected_ids).update(...)

#         return super().form_valid(form)
