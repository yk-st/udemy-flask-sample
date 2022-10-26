from distutils.log import Log
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

import logging
import os

class Config:

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{dbname}?charset=utf8'.format(**{
        'user': os.getenv('MYSQL_USER', ''),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'host': 'mysql_koz',
        'dbname': 'hoge'
    })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    # Assets Management
    SECRET_KEY = os.getenv('SECRET_KEY', '') 

    WTF_CSRF_ENABLED = True

    # DEBUG
    DEBUG_TB_INTERCEPT_REDIRECTS=False

    # jsonをそのままダンプする(ASCIIにしない)
    JSON_AS_ASCII = False

# さまざまな場所からアクセスするため外に出す
db = SQLAlchemy()

# blue printで作る
app = Flask(
    __name__,
    static_folder = "views/static",
    template_folder = "views/templates"
)

# api
api = Api(app)

def create_app():

    Configs = Config

    # config
    app.config.from_object(Configs)
    app.debug = True
    app.logger.setLevel(logging.DEBUG)

    # databaseのインスタンスを作成する
    # apps/model/configディレクトリにある場合はapps.model.config.Configとなる
    db.init_app(app)

    from apps.pymodule.social import index as social_api
    # 使い方は実は変わらない
    app.register_blueprint(social_api.social)

    from apps.pymodule.db import index as db_api
    # 使い方は実は変わらない
    app.register_blueprint(db_api.dbs)

    return app

@app.errorhandler(500)
def error_500(e):
    print('httpステータス:{}, メッセージ:{}, 詳細:{}'.format(e.code, e.name, e.description))
    return jsonify({'message': 'internal server error', 'action': 'サーバエラーが発生しました。しばらくしてからもう一度アクセスしてください。'}), 500

@app.errorhandler(404)
def error_404(e):
    print('httpステータス:{}, メッセージ:{}, 詳細:{}'.format(e.code, e.name, e.description))
    return jsonify({'message': 'ページが存在しないようです。URLをもう一度ご確認ください', 'action': 'ページが存在しないようです。URLをもう一度ご確認ください'}), 404