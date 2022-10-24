# -*- encoding: utf-8 -*-

from random import choices
from flask_wtf import FlaskForm
from wtforms import  IntegerField, SubmitField
from wtforms.validators import DataRequired



class MoneyBasicForm(FlaskForm):
    
    # 総資産
    soushisan = IntegerField('soushisan', default=0, validators=[DataRequired()])

    submit = SubmitField('保存')