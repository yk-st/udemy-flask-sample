from sqlalchemy import Column, ForeignKey, text, bindparam
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from werkzeug.security import generate_password_hash
from datetime import datetime, date

from apps.app import db

# 総資産の収支を管理するテーブル
class MONEY(db.Model):
    __tablename__ = "money"

    system_id = db.Column(db.String(256), primary_key=True, index=True)
    # 総資産
    soushisan = db.Column(db.Integer, default = 0)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def get_data(self):

        # sqlも書くことができます
        #sql = text("""
        #    select sum(soushisan) as earn from hoge.moeny where system_id = :system_id and update_at >= CURDATE()
        #    """).bindparams(bindparam('system_id', self.system_id))
        #return db.session.execute(sql).first()
        return MONEY.query.filter_by(system_id = self.system_id).first()
