from dataclasses import dataclass
from datetime import datetime
from flask import Blueprint, flash
from flask import render_template, request, redirect, url_for


from apps.app import db
from apps.pymodule.setting.models import MONEY
from apps.pymodule.setting.froms import MoneyBasicForm

setting = Blueprint('setting', 
        __name__, 
        url_prefix='/setting')

@setting.route('/', methods=["GET", "POST"])
def money():

        # フォーム
        form = MoneyBasicForm()

        # 有効なフォームの場合
        # Tokenが想定外だと処理に入らない
        if request.method == "POST" and form.validate_on_submit():

                money:MONEY = MONEY(
                        # 認証認可が入ると、この処理はリクエストヘッダーから取得することができる
                        system_id = "111111"
                )

                money = money.get_data()

                # 入力された総資産を設定
                if money is None:
                        # データがある場合とない場合で分けることができる
                        money = MONEY(
                                # 認証認可が入ると、この処理はリクエストヘッダーから取得することができる
                                system_id = "111111",
                                soushisan =  form.soushisan
                        )
                else:
                        money = form.soushisan.data

                # 更新と削除を兼ねることが可能
                db.session.add(money)
                # 削除
                #db.session.delete(money)
                db.session.commit()

        # 表示する内容を指定
        return render_template("setting/money_resource.html", form=form)