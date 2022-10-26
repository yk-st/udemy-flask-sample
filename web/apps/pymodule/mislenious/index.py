from dataclasses import dataclass
from datetime import datetime
from flask import Blueprint, flash
from flask import render_template, request
import logging

from apps.app import db
from apps.pymodule.setting.index import check_jwt
from apps.pymodule.mislenious.models import MANI_CAPITAL, SOCIAL_CAPITAL, HUMAN_CAPTAL, CHORES, ONESTEP_MASTER
from apps.pymodule.mislenious.form import SocialSocialForm, human_basic_form_builder, MoneyBasicForm, ChoreForm

setting = Blueprint('mislenious', 
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

@setting.route('/')
def mislenious():

        form = SocialSocialForm()

        # 初期値の設定を行う
        social_captal = SOCIAL_CAPITAL(
                system_id = check_jwt()
        )

        user_social_capital:SOCIAL_CAPITAL = social_captal.get_record()

        # レコードが撮れた場合は初期とを設定
        if user_social_capital is not None:
                form.frends_external.data = user_social_capital.friend_external
                form.frends_internal.data = user_social_capital.friend_internal

        # humanタブデータ
        humanform = human()
        # 
        moneyform = money()

        return render_template(
                setting.name + "/" + "social_resource.html", 
                form=form,
                humanform = humanform,
                moneyform = moneyform)

def human():

        human_captal = HUMAN_CAPTAL(
                system_id = check_jwt()
        )

        # 既に登録データがあるかチェック
        user_human_captal:HUMAN_CAPTAL = human_captal.get_record()

        onestep_master:ONESTEP_MASTER = ONESTEP_MASTER.getall()

        onesteplist = []
        form = None

        # 初回登録以外
        if user_human_captal is not None:

                #List dic形式
                for onestep in user_human_captal.onestep_staus:
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
                gakurekiClass.checked = user_human_captal.gakureki

                #人的資本はビルダーでビルドする
                form = human_basic_form_builder(onesteplist, gakurekiClass)

                # 誕生日
                form.birth_day.data = user_human_captal.birth_day

        else:
                # マスターからのデータを利用する
                onesteplist = onestep_master
                
                # 学歴オブジェクトの作成
                gakurekiClass = Gakureki()
                #人的資本はビルダーでビルドする
                form = human_basic_form_builder(onesteplist, gakurekiClass)

        return form

def money():

        form = MoneyBasicForm()

        mani_captal:MANI_CAPITAL = MANI_CAPITAL(
                system_id = check_jwt()
        )

        mani_captal_record:MANI_CAPITAL = mani_captal.get_record()

        # お手伝いテーブルの取得
        chores:CHORES = CHORES(
                system_id = check_jwt()
        )

        chores_record:CHORES = chores.get_record()

        # 既に登録データが存在する場合は初期フォームに設定
        if mani_captal_record is not None:

                form.kozukaidate.data = mani_captal_record.okozukai_date
                form.kozukaimani.data = mani_captal_record.okozukai
                # お手伝いリスト
                # form.chorelist.data = chores_record.chore_maniはできないのでappend_entryする
                for chore in chores_record.chore_mani:
                        choreobj = ChoreForm()
                        # デフォルト値を変更する
                        choreobj.chore = chore["chore"]
                        choreobj.mani = chore["mani"]
                        # max で append するとエラー
                        form.chorelist.append_entry(choreobj)
        else:
                # 入れ物だけを作る
                for chore in range(15):
                        choreobj = ChoreForm()
                        # デフォルト値を変更する
                        choreobj.chore = None
                        choreobj.mani = 0
                        # max で append するとエラー
                        form.chorelist.append_entry(choreobj)

        return form


@setting.route('/save/mislenious/<page>', methods=["GET", "POST"])
def save_social(page):

        form = SocialSocialForm()

        if request.method == "POST" and form.validate_on_submit():

                social_captal = SOCIAL_CAPITAL(
                        system_id = check_jwt()
                )

                user_social_capital:SOCIAL_CAPITAL = social_captal.get_record()

                # 登録データが存在していない場合
                if user_social_capital is None:
                        user_social_capital = SOCIAL_CAPITAL(
                                system_id = check_jwt(),
                                friend_internal = form.frends_internal.data,
                                friend_external = form.frends_external.data,
                                social_score = 10
                        )
                else:
                        user_social_capital.friend_internal = form.frends_internal.data,
                        user_social_capital.friend_external = form.frends_external.data,

                db.session.add(user_social_capital)
                db.session.commit()

                flash("データが保存されました。")
        else:
                flash("無効なフォーム送信です")

        return render_template(setting.name + "/" + "social_resource.html", form=form)

@setting.route('/save/mislenious/<page>', methods=["GET", "POST"])
def save_human(page):

        oneseplist:ONESTEP_MASTER = None
        # マスターデータからデータを取得
        oneseplist:ONESTEP_MASTER = ONESTEP_MASTER.getall()

        gakurekiClass = Gakureki()

        #人的資本はビルダーでビルドしつつデータを保管してゆく
        form = human_basic_form_builder(oneseplist, gakurekiClass)

        if request.method == "POST" and form.validate_on_submit():

                onestep_status = []
                # onestep statusの作成
                for onestep in form.onestep_checkbox:
                        print(form[onestep])
                        onestep_status.append({
                                "onestep_id": onestep.split(":")[1] ,
                                "checked": form[onestep].data})

                human_captal:HUMAN_CAPTAL = HUMAN_CAPTAL(
                        system_id = check_jwt()
                )

                # 人的資本取得
                human_capital_record:HUMAN_CAPTAL = human_captal.get_record()   

                # 初期登録の場合
                if human_capital_record is None:
                        human_capital_record:HUMAN_CAPTAL = HUMAN_CAPTAL(
                                system_id = check_jwt(),
                                birth_day = form.birth_day.data,
                                gakureki = form.gakureki_radio.data,
                                onestep_staus = onestep_status,
                                human_score = 10,
                                # TODO 年齢の計算
                                age = 11
                        )
                else:   
                        human_capital_record.onestep_staus = onestep_status
                        human_capital_record.birth_day = form.birth_day.data
                        human_capital_record.gakureki = form.gakureki_radio.data
                        human_capital_record.human_score = 11

                # データベースへの反映(いまいち動かん。。)
                db.session.add(human_capital_record)
                db.session.commit()

                flash("登録が完了しました")
        else:
                flash("無効なフォーム送信です")

        return render_template(setting.name + "/" + "human_resource.html", form=form)

@setting.route('/save/mislenious/<page>', methods=["GET", "POST"])
def save_money(page):

        form:MoneyBasicForm = MoneyBasicForm()

        if request.method == "POST" and form.validate_on_submit():

                mani_captal:MANI_CAPITAL = MANI_CAPITAL(
                        system_id = check_jwt()
                )

                mani_captal_record:MANI_CAPITAL = mani_captal.get_record()

                # お手伝いテーブルの登録
                chores:CHORES = CHORES(
                        system_id = check_jwt()
                )

                chores_record:CHORES = chores.get_record()

                # 初回登録の場合
                if mani_captal_record is None:
                        mani_captal_record = MANI_CAPITAL(
                                system_id = check_jwt(),
                                okozukai = form.kozukaimani.data,
                                okozukai_date = form.kozukaidate.data,
                                mani_score = 10
                        )

                        chores_record = CHORES(
                                system_id = check_jwt(),
                                chore_mani = form.chorelist.data
                        )
                else:

                        mani_captal_record.okozukai_date = form.kozukaidate.data,
                        mani_captal_record.okozukai = form.kozukaimani.data
                        mani_captal_record.mani_score = 11

                        chores_record.chore_mani = form.chorelist.data
                
                db.session.add(mani_captal_record)
                db.session.add(chores_record)
                db.session.commit()

                flash("登録が完了しました")
                
        else:
                flash("無効なフォーム送信です")
        
        return render_template(setting.name + "/" + "money_resource.html", form=form)
