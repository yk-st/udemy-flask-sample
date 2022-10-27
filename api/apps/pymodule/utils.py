# -*- coding: utf-8 -*-
from flask import request
import jwt
import os
from apps.app import api
from functools import wraps
from keycloak import KeycloakOpenID

keycloak_openid = KeycloakOpenID(server_url="https://auth.udemy-flask-sample.top:8443/",
                                 client_id="flasks",
                                 realm_name="hogepeke",
                                 client_secret_key=os.getenv('CLIENT_SECRET', ''))

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

                # キーがデコードできるかチェックする(ローカルチェックでもOKだが)
                # jwt.decode(
                #     request.headers["X-Access-Token"],
                #     public_key,
                #     algorithms=["RS256"],
                #     audience="flasks",
                #     issuer="https://auth.udemy-flask-sample.top:8443/realms/hogepeke")
                # expireのチェックなども入れる

                #　イントロスペクションを行うエンドポイントを追加するとよりベター
                token_info = keycloak_openid.introspect(request.headers["X-Access-Token"])

                # アクティブじゃない場合はNg
                if not token_info['active']:
                    print("NGです。")
                    api.abort(403)

                #print(token_info)
                #{'exp': 1666850209, 'iat': 1666843009, 'jti': '98c0adef-d806-444b-a0da-5c2ff21ec0d7', 
                # 'iss': 'https://auth.udemy-flask-sample.top:8443/realms/hogepeke',
                #  'aud': ['flasks', 'account'], 
                # 'sub': 'cafab263-01cb-4e02-89a1-9d96a1a8996f', 
                # 'typ': 'Bearer', 'azp': 'flasks', 
                # 'preferred_username': 'service-account-flasks', 
                # 'email_verified': False, 'acr': '1',
                #  'realm_access': {'roles': ['offline_access', 'default-roles-hogepeke', 'uma_authorization']}, 
                # 'resource_access': {'account': {'roles': ['manage-account', 'manage-account-links', 'view-profile']}}, 
                # 'scope': 'openid email profile', 'clientHost': '118.27.18.23', 
                # 'clientId': 'flasks', 'clientAddress': '118.27.18.23', 'client_id': 
                # 'flasks', 'username': 'service-account-flasks', 'active': True}

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
