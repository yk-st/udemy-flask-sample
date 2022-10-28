from sqlalchemy import Column, ForeignKey, text, bindparam
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from werkzeug.security import generate_password_hash
from datetime import datetime, date

from apps.app import db

class CHECK_BOX(db.Model):
    __tablename__ = "check_box"

    system_id = db.Column(db.String(256) , primary_key=True)
    gakureki = db.Column(db.Integer)
    # onestep_id:True,False
    onestep_staus = db.Column(db.JSON())
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def get_record(self):
        return CHECK_BOX.query.filter_by(system_id = self.system_id).first()


class ONESTEP_MASTER(db.Model):
    __tablename__ = "onestep_master"

    onestep_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    description = db.Column(db.String(256))
    checked = db.Column(db.Boolean, default=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def getall():
        return ONESTEP_MASTER.query.all()

class OTOMODATI(db.Model):
    __tablename__ = "otomodati"

    system_id = db.Column(db.String(256) , primary_key=True)
    friend_internal = db.Column(db.Integer, default=0)
    friend_external =  db.Column(db.Integer, default=0)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def get_record(self):
        return OTOMODATI.query.filter_by(system_id = self.system_id).first()

# お手伝い
class CHORES(db.Model):
    __tablename__ = "chores"

    chore_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    # TODO 外部キー
    system_id = db.Column(db.String(256), primary_key=True, index=True)
    # chore:mani
    chore_mani = db.Column(db.JSON())
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def get_record(self):
        return CHORES.query.filter_by(system_id = self.system_id).first()