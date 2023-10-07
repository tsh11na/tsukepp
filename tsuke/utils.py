from django.db import transaction
from django.utils import timezone

from .models import Tsuke


@transaction.atomic
def settle(tsuke_ids):
    """
    決済処理
    
    Parameters
    ----------
    tsuke_ids: list[int]
        決済するツケのid
    
    Returns
    -------
    bool
        更新処理が成功したかどうか
    """

    try: # 更新処理
        # 決済対象のツケを取得
        checking_tsuke_list = Tsuke.objects.filter(id__in=tsuke_ids)
        now = timezone.now()

        # 清算済に変更
        for tsuke in checking_tsuke_list:
            tsuke.is_paid = True
            tsuke.payment_date = now

        Tsuke.objects.bulk_update(checking_tsuke_list, fields=["is_paid", "payment_date"])

    except(KeyError, Tsuke.DoesNotExist):
        # TODO エラー処理
        return False

    else:  # 成功時
        return True
