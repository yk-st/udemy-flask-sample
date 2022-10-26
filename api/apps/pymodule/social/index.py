from tkinter import TRUE
from flask import Blueprint,request
from flask_restx import Resource, fields
from apps.app import api, db
from apps.pymodule.utils import check_token
import json

social = Blueprint('social', 
        __name__, 
        url_prefix='/social')

# namespaceを追加
social_nm = api.namespace('api/v1', description='social')

# response
responses_dic = {200: 'Ping Success', 201: 'Process Success', 403: 'Not Authorized', 500: 'Internal Server Error'}

# 以下レスポンス定義

# カスタムフィールドで対応する
# https://github.com/python-restx/flask-restx/issues/115
class DictItem(fields.Raw):
    def output(self, key, obj, *args, **kwargs):
        try:
                #alchemyのattr
                dct = getattr(obj, self.attribute)
        except AttributeError:
            return {}
        return dct or {}

# モデルのベースを作成
resource_base = {}
resource_base['id'] = fields.String(readonly=True,
                        description='The task unique identifier',
                        example='fdc02467-67df-4577-9ceb-d9a18acc0587',
                        require=True)
resource_base['address'] = DictItem(attribute='address')

# 入れ子の中のデータを定義する
nested_resource = {}
nested_resource['id'] = fields.Integer
nested_resource['zip'] = fields.String
nested_resource['postal'] = fields.String

resource_base['addresses'] = fields.List(fields.Nested(nested_resource))

# モデル作成
model = social_nm.model('hoge', resource_base)

# SQLAlchemyとして用意すればいい
class hoge(db.Model):

        __tablename__ = "hoge"

        id=db.Column(db.String(256) , primary_key=True)
        address=db.Column(db.JSON())

        def get_record(self):
                self.id ='aaa'
                self.address= {"zip": "peke", "postal": "maruo"}
                self.addresses= [{"id": 1, "zip": "peke", "postal": "maruo"}, {"id": 2, "zip": "pekeo", "postal": "maruo2"}]
                return self

@social_nm.route('/social')
class index(Resource):

        # サーフェイスコントロール(トークンがない、必須項目が入ってないなど)はデコレーターで実施する
        #　ビジネスコントロールとそのエラーは内部で行う
        # 202 accepted 200はpingが通ったくらいのイメージ 201は処理したよ。というイメージで使われることが多い。
        # 予測可能にする：Languageで言語変えたりとかも入れても良い

        @social_nm.doc('get_social_data', responses=responses_dic)
        @social_nm.marshal_with(model, envelope='resource')
        @check_token
        def get(self):
                # marshalを使うと、return時に値をラッピングしてくれる
                return hoge().get_record()

        @social_nm.doc(responses=responses_dic)
        @check_token
        def post(self):
                return {'hello': 'post'}
