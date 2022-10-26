# -*- encoding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import Email, DataRequired, length

class InquryForm(FlaskForm):
    username = StringField('お名前',
                         id='username_login',
                         validators=[
                             DataRequired(),
                             length(max=30, message = "30文字以内で入力してください")])
    company = StringField('会社・事業所名',
                         id='username_login',
                         validators=[
                             length(max=30, message = "30文字以内で入力してください")])
    email = StringField('メールアドレス',
                         id='username_login',
                         validators=[
                             DataRequired(),
                             Email()])
    inqury = TextAreaField('お問合せ',
                         id='inqury',
                         validators=[
                             DataRequired()
                             ])
