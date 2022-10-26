from dataclasses import dataclass
from datetime import datetime
from flask import Blueprint, flash
from flask import render_template, request, redirect, url_for

import jwt
import os
from apps.app import db, app
from apps.pymodule.setting.models import MONEY
from apps.pymodule.setting.froms import MoneyBasicForm

setting = Blueprint('setting', 
        __name__, 
        url_prefix='/setting')

@setting.route('logout', methods=["GET", "POST"])
def logout():
    
    # logoutのエンドポイントを呼び出す
    return redirect("https://udemy-flask-sample.top/oauth2/sign_out?rd=https%3A%2F%2Fauth.udemy-flask-sample.top%3A8443%2Frealms%2Fhogepeke%2Fprotocol%2Fopenid-connect%2Flogout/")

@setting.route('check_jwt', methods=["GET", "POST"])
def check_jwt():
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

@setting.route('/', methods=["GET", "POST"])
def money():

        app.logger.warning("hoge")

        # フォーム
        form = MoneyBasicForm()

        # 有効なフォームの場合
        # Tokenが想定外だと処理に入らない
        if request.method == "POST" and form.validate_on_submit():

                money:MONEY = MONEY(
                        # 認証認可が入ると、この処理はリクエストヘッダーから取得することができる
                        system_id = check_jwt()
                )

                money_record = money.get_data()

                # 入力された総資産を設定
                if money_record is None:
                        # データがある場合とない場合で分けることができる
                        money_record = MONEY(
                                # 認証認可が入ると、この処理はリクエストヘッダーから取得することができる
                                system_id = check_jwt(),
                                soushisan =  form.soushisan.data
                        )
                else:
                        money_record.soushisan = form.soushisan.data

                # 更新と削除を兼ねることが可能
                db.session.add(money_record)
                # 削除
                #db.session.delete(money_record)
                db.session.commit()

                # flash メッセージ
                flash("登録完了しました。")

        # 表示する内容を指定
        return render_template("setting/money_resource.html", form=form)