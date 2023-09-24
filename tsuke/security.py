"""多重送信防止など、セキュリティ関連の設定"""
# https://qiita.com/hamemi/items/d6cb8e0d60821a7e89aa

import uuid


def set_submit_token(request):
    """トークンを設定する"""
    submit_token = str(uuid.uuid4())
    request.session['submit_token'] = submit_token
    return submit_token

def is_valid_token(request):
    """トークンの有効性を確認する"""
    token_in_request = request.POST.get('submit_token')
    token_in_session = request.session.pop('submit_token', '')

    if (not token_in_request) or (not token_in_session):
        return False

    return token_in_request == token_in_session
