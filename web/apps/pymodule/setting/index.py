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
        if request.method == "POST" and form.validate_on_submit():

                moey:MONEY = MONEY(
                        # 認証認可が入ると、この処理はリクエストヘッダーから取得することができる
                        system_id = "111111"
                )

                moey:MONEY = moey.get_record()

        return render_template("setting/money_resource.html", form=form)