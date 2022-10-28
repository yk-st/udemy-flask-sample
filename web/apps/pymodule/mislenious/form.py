# -*- encoding: utf-8 -*-

from random import choices
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, DateField, RadioField, FormField, FieldList, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class BasicForm(FlaskForm):
    frends_internal = IntegerField('internal_friend',
                         id='internal_friend',
                         validators=[
                             DataRequired(),
                             NumberRange(min=0)])

    frends_external = IntegerField('external_friend',
                         id='external_friend',
                         validators=[
                             NumberRange(min=0)])

    submit = SubmitField('保存')

class HumanBasicFormBase(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(HumanBasicFormBase, self).__init__(*args, **kwargs)

def checkbox_builder(onesteplist, gakurekiClass):

    class HumanBasicForm(HumanBasicFormBase):
        pass

    # チェックボックスは少し特殊(FieldListが使えない)
    onestep_checkbox = []
    for (i, onestep) in enumerate(onesteplist):
        setattr(
            HumanBasicForm,
            'onestep_checkbox:%d' % onestep.onestep_id,
            BooleanField(
                label = onestep.description,
                id = 'onestep_checkbox_%d' % onestep.onestep_id,
                validators=[],
                default=onestep.checked
            )
        )
        onestep_checkbox.append('onestep_checkbox:%d' % onestep.onestep_id)

    setattr(HumanBasicForm, 'onestep_checkbox', onestep_checkbox)

    # 学歴ラジオボタン
    gakureki_raido = RadioField(
            "gakureki_radio",
            choices=gakurekiClass.gakurekilist,
            validators=[DataRequired()],
            default=gakurekiClass.checked
        )
    setattr(HumanBasicForm, 'gakureki_radio', gakureki_raido)

    return HumanBasicForm()

class ChoreForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        #kwargs['csrf_enabled'] = False  # 子フォームではCSRFトークンが生成されないように設定
        super(ChoreForm, self).__init__(*args, **kwargs)

    chore = StringField('chore', default=None, validators=[])
    okozukai = IntegerField('okozukai', default=0, validators=[])

class MoneyBasicForm(FlaskForm):

    # お手伝いリスト(return list dict)
    # リストを作る時にはフィールドリスト（フォームを複数個使う場合）
    chorelist = FieldList(FormField(ChoreForm, 'Member'), min_entries=0, max_entries=15)

    submit = SubmitField('保存')

