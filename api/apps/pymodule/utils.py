# -*- coding: utf-8 -*-
from flask import request
import jwt
import os
from apps.app import api
from functools import wraps

def check_token(func):

    @wraps(func)
    def token(*args, **kwargs):
        print(request.headers)
        # Token　チェック
        if "X-Access-Token" in request.headers:
            print("hoge")
            # JWTをデコードするためのパブリックキー
            public_key_body = os.getenv('JWT_PUBLIC_KEY', '')
            public_key = "-----BEGIN PUBLIC KEY-----\n" \
                            + public_key_body \
                            + "\n-----END PUBLIC KEY-----"
            try:

                # キーがデコードできるかチェックする(ローカルチェック)
                jwt.decode(
                    request.headers["X-Access-Token"],
                    public_key,
                    algorithms=["RS256"],
                    audience="flasks",
                    issuer="https://auth.udemy-flask-sample.top:8443/realms/hogepeke")["sub"]

                #　イントロスペクションを行うエンドポイントを追加するとよりベター

            except Exception as e:
                print(e)
                api.abort(403)
            
        else:
            api.abort(403)

        return func(*args, **kwargs)

    return token


def get_jwt():
    # JWTをデコードするためのパブリックキー
    public_key_body = os.getenv('JWT_PUBLIC_KEY', '')
    public_key = "-----BEGIN PUBLIC KEY-----\n" \
                    + public_key_body \
                    + "\n-----END PUBLIC KEY-----"

    #   File "/usr/local/lib/python3.10/site-packages/jwt/api_jwt.py", line 234, in _validate_exp
    #     raise ExpiredSignatureError("Signature has expired")
    # jwt.exceptions.ExpiredSignatureError: Signature has expired
    # [pid: 8|app: 0|req: 6/6] 172.16.0.3 () {66 vars in 6234 bytes} [Wed Sep 28 20:40:15 2022] GET /dashboard/ => generated 0 bytes in 11 msecs (HTTP/1.0 500) 0 headers in 0 bytes (0 switches on core 0)
    # 例えば期限切れの場合はこんなログが出る
    
    # issureとaudienceもチェックを行う
    # 変なissureのトークンをエンコードしようとするとエラーになる
    sub = jwt.decode(
        request.headers["X-Access-Token"],
        public_key,
        algorithms=["RS256"],
        audience="flasks",
        issuer="https://auth.udemy-flask-sample.top:8443/realms/hogepeke")["sub"]

    return sub
