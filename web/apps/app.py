from distutils.log import Log
from flask import Flask, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_login import LoginManager

import importlib
import logging
import os
from datetime import timedelta

# blue printで作る
app = Flask(
    __name__,
    static_folder = "views/static",
    template_folder = "views/templates"
)

def create_app():

    from apps.pymodule.landing import index as landing_view
    app.register_blueprint(landing_view.landing)

    return app

@app.errorhandler(500)
def error_500(e):
    print('httpステータス:{}, メッセージ:{}, 詳細:{}'.format(e.code, e.name, e.description))
    return jsonify({'message': 'internal server error', 'action': 'サーバエラーが発生しました。しばらくしてからもう一度アクセスしてください。'}), 500

@app.errorhandler(404)
def error_404(e):
    print('httpステータス:{}, メッセージ:{}, 詳細:{}'.format(e.code, e.name, e.description))
    return jsonify({'message': 'ページが存在しないようです。URLをもう一度ご確認ください', 'action': 'ページが存在しないようです。URLをもう一度ご確認ください'}), 404