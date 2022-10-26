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
                print(e.with_traceback)
                api.abort(403)
            
        else:
            api.abort(403)

        return func(*args, **kwargs)

    return token
