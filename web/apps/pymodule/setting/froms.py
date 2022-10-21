# -*- encoding: utf-8 -*-

from random import choices
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, DateField, RadioField, FormField, FieldList, SelectField, SubmitField
from wtforms.validators import Email, DataRequired, length, NumberRange



class MoneyBasicForm(FlaskForm):

    # 総資産
    soushisan = IntegerField('money', default=0, validators=[DataRequired()])

    submit = SubmitField('保存')