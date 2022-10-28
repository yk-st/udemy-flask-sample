from dataclasses import dataclass
from datetime import datetime
from flask import Blueprint, flash
from flask import render_template, request
import logging

from apps.app import db
from apps.pymodule.setting.index import check_jwt
from apps.pymodule.mislenious.models import OTOMODATI, CHECK_BOX, CHORES, ONESTEP_MASTER
from apps.pymodule.mislenious.form import BasicForm, checkbox_builder, MoneyBasicForm, ChoreForm

mislenious = Blueprint('mislenious', 
        __name__, 
        url_prefix='/mislenious')

# 学歴クラス
class Gakureki():

        def __init__(self):
                # 学歴
                self.gakurekilist = [
                        ("1", "中卒"),
                        ("2", "高卒"),
                        ("3", "大卒"),
                        ("4", "院卒"),
                        ("5", "博士")
                ]
                self.checked = 1

@mislenious.route('/')
def index():

        basicform = basic()
        # humanタブデータ
        checkboxform = checkbox()
        # 
        moneyform = money()

        return render_template(
                mislenious.name + "/" + "money_resource.html", 
                basicform=basicform,
                checkboxform = checkboxform,
                moneyform = moneyform)

def basic():

        form = BasicForm()
        # 初期値の設定を行う
        otomodati = OTOMODATI(
                system_id = check_jwt()
        )

        user_otomodati:OTOMODATI = otomodati.get_record()

        # レコードが撮れた場合は初期とを設定
        if user_otomodati is not None:
                form.frends_external.data = user_otomodati.friend_external
                form.frends_internal.data = user_otomodati.friend_internal

        return form

def checkbox():

        check_box = CHECK_BOX(
                system_id = check_jwt()
        )

        # 既に登録データがあるかチェック
        user_check_box:CHECK_BOX = check_box.get_record()

        onestep_master:ONESTEP_MASTER = ONESTEP_MASTER.getall()

        onesteplist = []
        form = None

        # 初回登録以外
        if user_check_box is not None:

                #List dic形式
                for onestep in user_check_box.onestep_staus:
                        for master in onestep_master:
                                # キーが一緒のものを取得
                                if onestep["onestep_id"] == str(master.onestep_id):
                                        # 登録データの作成
                                        append_data = ONESTEP_MASTER(
                                                onestep_id = master.onestep_id,
                                                description = master.description,
                                                checked = onestep["checked"]
                                        )
                                        onesteplist.append(append_data)
                                        break

                # 学歴オブジェクトの作成
                gakurekiClass = Gakureki()
                gakurekiClass.checked = user_check_box.gakureki

                #チェックボックス
                form = checkbox_builder(onesteplist, gakurekiClass)

        else:
                # マスターからのデータを利用する
                onesteplist = onestep_master
                
                # 学歴オブジェクトの作成
                gakurekiClass = Gakureki()
                #チェックボックス
                form = checkbox_builder(onesteplist, gakurekiClass)

        return form

def money():

        form = MoneyBasicForm()

        # お手伝いテーブルの取得
        chores:CHORES = CHORES(
                system_id = check_jwt()
        )

        chores_record:CHORES = chores.get_record()

        # 既に登録データが存在する場合は初期フォームに設定
        if chores_record is not None:

                # お手伝いリスト
                # form.chorelist.data = chores_record.chore_maniはできないのでappend_entryする
                for chore in chores_record.chore_mani:
                        choreobj = ChoreForm()
                        # デフォルト値を変更する
                        choreobj.chore = chore["chore"]
                        choreobj.okozukai = chore["okozukai"]
                        # max で append するとエラー
                        form.chorelist.append_entry(choreobj)
        else:
                # 入れ物だけを作る
                for chore in range(15):
                        choreobj = ChoreForm()
                        # デフォルト値を変更する
                        choreobj.chore = None
                        choreobj.okozukai = 0
                        # max で append するとエラー
                        form.chorelist.append_entry(choreobj)

        return form


@mislenious.route('/save/mislenious/basic/<page>', methods=["GET", "POST"])
def save_form(page):

        basicform = BasicForm()

        if request.method == "POST" and basicform.validate_on_submit():

                otomodati = OTOMODATI(
                        system_id = check_jwt()
                )

                user_otomodati:OTOMODATI = otomodati.get_record()

                # 登録データが存在していない場合
                if user_otomodati is None:
                        user_otomodati = OTOMODATI(
                                system_id = check_jwt(),
                                friend_internal = basicform.frends_internal.data,
                                friend_external = basicform.frends_external.data,
                        )
                else:
                        user_otomodati.friend_internal = basicform.frends_internal.data,
                        user_otomodati.friend_external = basicform.frends_external.data,

                db.session.add(user_otomodati)
                db.session.commit()

                flash("データが保存されました。")
        else:
                flash("無効なフォーム送信です")

        # 他のタブのデータ
        checkboxform = checkbox()
        moneyform = money()

        return render_template(
                mislenious.name + "/" + "money_resource.html",
                basicform=basicform,
                checkboxform = checkboxform,
                moneyform = moneyform)

@mislenious.route('/save/mislenious/radio/<page>', methods=["GET", "POST"])
def save_radio_checkbox(page):

        oneseplist:ONESTEP_MASTER = None
        # マスターデータからデータを取得
        oneseplist:ONESTEP_MASTER = ONESTEP_MASTER.getall()

        gakurekiClass = Gakureki()

        #ビルダーでビルドしつつデータを保管してゆく
        checkboxform = checkbox_builder(oneseplist, gakurekiClass)

        if request.method == "POST" and checkboxform.validate_on_submit():

                onestep_status = []
                # onestep statusの作成
                for onestep in checkboxform.onestep_checkbox:
                        print(checkboxform[onestep])
                        onestep_status.append({
                                "onestep_id": onestep.split(":")[1] ,
                                "checked": checkboxform[onestep].data})

                check_box:CHECK_BOX = CHECK_BOX(
                        system_id = check_jwt()
                )

                
                checkbox_record:CHECK_BOX = check_box.get_record()   

                # 初期登録の場合
                if checkbox_record is None:
                        checkbox_record:CHECK_BOX = CHECK_BOX(
                                system_id = check_jwt(),
                                gakureki = checkboxform.gakureki_radio.data,
                                onestep_staus = onestep_status,
                        )
                else:   
                        checkbox_record.onestep_staus = onestep_status
                        checkbox_record.gakureki = checkboxform.gakureki_radio.data

                # データベースへの反映
                db.session.add(checkbox_record)
                db.session.commit()

                flash("登録が完了しました")
        else:
                flash("無効なフォーム送信です")

        basicform = basic()
        moneyform = money()

        return render_template(
                mislenious.name + "/" + "money_resource.html",
                basicform=basicform,
                checkboxform = checkboxform,
                moneyform = moneyform)

@mislenious.route('/save/mislenious/money/<page>', methods=["GET", "POST"])
def save_form_list(page):

        moenyform:MoneyBasicForm = MoneyBasicForm()

        if request.method == "POST" and moenyform.validate_on_submit():

                # お手伝いテーブルの登録
                chores:CHORES = CHORES(
                        system_id = check_jwt()
                )

                chores_record:CHORES = chores.get_record()

                # 初回登録の場合
                if chores_record is None:
                        chores_record = CHORES(
                                system_id = check_jwt(),
                                chore_mani = moenyform.chorelist.data
                        )
                else:
                        chores_record.chore_mani = moenyform.chorelist.data
                
                db.session.add(chores_record)
                db.session.commit()

                flash("登録が完了しました")
                
        else:
                flash("無効なフォーム送信です")
        
        checkboxform = checkbox()
        basicform = basic()

        return render_template(
                mislenious.name + "/" + "money_resource.html",
                basicform=basicform,
                checkboxform = checkboxform,
                moneyform = moenyform)
