from sqlalchemy import Column, ForeignKey, text, bindparam
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from werkzeug.security import generate_password_hash
from datetime import datetime, date

from apps.app import db

class HUMAN_CAPTAL(db.Model):
    __tablename__ = "human_capital"

    system_id = db.Column(db.BigInteger , primary_key=True)
    birth_day = db.Column(db.DateTime)
    age = db.Column(db.Integer)
    gakureki = db.Column(db.Integer)
    # onestep_id:True,False
    onestep_staus = db.Column(db.JSON())
    human_score = db.Column(db.BigInteger)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def birth2age(self):
        today = date.today()
        # 誕生日から現在の年齢を計算
        #self.age = (int(today.strftime("%Y%m%d")) - int(self.birth_day.strftime("%Y%m%d"))) 
        self.age = 11

    def get_record(self):
        return HUMAN_CAPTAL.query.filter_by(system_id = self.system_id).first()


class ONESTEP_MASTER(db.Model):
    __tablename__ = "onestep_master"

    onestep_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    description = db.Column(db.String(256))
    checked = db.Column(db.Boolean, default=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def getall():
        return ONESTEP_MASTER.query.all()

class SOCIAL_CAPITAL(db.Model):
    __tablename__ = "social_capital"

    system_id = db.Column(db.BigInteger , primary_key=True)
    friend_internal = db.Column(db.Integer, default=0)
    friend_external =  db.Column(db.Integer, default=0)
    social_score = db.Column(db.BigInteger)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def get_record(self):
        return SOCIAL_CAPITAL.query.filter_by(system_id = self.system_id).first()

class MANI_CAPITAL(db.Model):
    __tablename__ = "mani_capital"

    system_id = db.Column(db.BigInteger , primary_key=True)
    okozukai_date = db.Column(db.String(64))
    okozukai = db.Column(db.BigInteger)
    mani_score = db.Column(db.BigInteger)
    # 現状いくら持っているか
    mani = db.Column(db.BigInteger)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def get_record(self):
        return MANI_CAPITAL.query.filter_by(system_id = self.system_id).first()

# maniの収支を管理するテーブル
class MANI(db.Model):
    __tablename__ = "mani"

    mani_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    # TODO 外部キー
    system_id = db.Column(db.BigInteger, primary_key=True, index=True)
    # Type 毎月のお小遣い:1、お手伝いによるもの:2、運用による損益:3
    earn_type = db.Column(db.Integer, default = None)
    # いくらもらったか
    earned =  db.Column(db.BigInteger, default = 0)
    # 何でいくらもらったか
    earn_from = db.Column(db.String(256), default = None)
    # expense 交換した:1
    expense_type = db.Column(db.Integer, default = None)
    # いくら使ったか
    expense = db.Column(db.BigInteger, default = 0)
    # 何に使ったか
    expense_to = db.Column(db.String(256), default = None)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def get_today_mani(self):

        sql = text("""
            select sum(earned) as earn from moneys.mani where system_id = :system_id and update_at >= CURDATE()
            """).bindparams(bindparam('system_id', self.system_id))

        return db.session.execute(sql).first()

# お手伝い
class CHORES(db.Model):
    __tablename__ = "chores"

    chore_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    # TODO 外部キー
    system_id = db.Column(db.BigInteger, primary_key=True, index=True)
    # chore:mani
    chore_mani = db.Column(db.JSON())
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def get_record(self):
        return CHORES.query.filter_by(system_id = self.system_id).first()