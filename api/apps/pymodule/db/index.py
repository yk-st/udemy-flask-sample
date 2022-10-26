from tkinter import TRUE
from flask import Blueprint,request
from flask_restx import Resource, fields
from apps.app import api, db
from apps.pymodule.utils import check_token, get_jwt
from apps.pymodule.db.models import MONEY
import json

dbs = Blueprint('dbs', 
        __name__, 
        url_prefix='/dbs')

# namespaceを追加
dbs_nm = api.namespace('api/v1', description='db')
# response
responses_dic = {200: 'Ping Success', 201: 'Process Success', 403: 'Not Authorized', 500: 'Internal Server Error'}

# モデルのベースを作成
resource_base = {}
resource_base['system_id'] = fields.String(readonly=True,
                        description='The task unique identifier',
                        example='fdc02467-67df-4577-9ceb-d9a18acc0587',
                        require=True)
resource_base['soushisan'] = fields.String(readonly=True,
                        description='The task unique identifier',
                        example='fdc02467-67df-4577-9ceb-d9a18acc0587',
                        require=True)
resource_base['create_at'] = fields.String(readonly=True,
                        description='The task unique identifier',
                        example='fdc02467-67df-4577-9ceb-d9a18acc0587',
                        require=True)
resource_base['update_at'] = fields.String(readonly=True,
                        description='The task unique identifier',
                        example='fdc02467-67df-4577-9ceb-d9a18acc0587',
                        require=True)

# モデル作成
model = dbs_nm.model('hoge', resource_base)

# 以下レスポンス定義
@dbs_nm.route('/dbs')
class index(Resource):

        # サーフェイスコントロール(トークンがない、必須項目が入ってないなど)はデコレーターで実施する
        #　ビジネスコントロールとそのエラーは内部で行う
        # 202 accepted 200はpingが通ったくらいのイメージ 201は処理したよ。というイメージで使われることが多い。
        # 予測可能にする：Languageで言語変えたりとかも入れても良い

        @dbs_nm.doc('get_sdbs_data', responses=responses_dic)
        @dbs_nm.marshal_with(model, envelope='money')
        @check_token
        def get(self):
                # marshalを使うと、return時に値をラッピングしてくれる
                money = MONEY( 
                        #system_id = get_jwt()
                        system_id = '9d9d33e0-bb8f-4724-99d9-807cf8b91cdb'
                )
                print(money.system_id)
                return money.get_data()
