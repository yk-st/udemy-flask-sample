from flask import Blueprint
from flask import render_template, request, flash, current_app
from apps.app import db, mail
from apps.pymodule.inqury.forms import InquryForm
from flask_mail import Mail, Message


inqury = Blueprint('inqury', 
        __name__, 
        url_prefix='/inqury')

@inqury.route('/')
def index():

        inqryform = InquryForm()
        return render_template(inqury.name + "/inqury.html", form = inqryform)

@inqury.route('/complete', methods=["GET", "POST"])
def complete():

        inqryform = InquryForm()
        if request.method == "POST" and inqryform.validate_on_submit():

                username = inqryform.username.data
                company = inqryform.company.data
                email = inqryform.email.data
                inqury_form = inqryform.inqury.data

                send_email(email, '問い合わせを受け付けました。', inqury.name + "/contact", username=username, company=company, inqury_form=inqury_form)
                # admin向けにメールを送る
                send_email(current_app.config['MAIL_USERNAME'], '問い合わせがきました。内容を確認しましょう', inqury.name + "/contact", username=username, company=company, inqury_form=inqury_form)

                # データベースに保存する処理を入れてもOK。

                flash("問い合わせ完了です。ありがとうございました。確認後返信させていただきます")

        return render_template(inqury.name + "/inqury.html", form = inqryform)

# 問い合わせメールを送る
def send_email(to, subject, template, **kwargs):
        msg = Message(subject, recipients=[to])
        msg.body = render_template(template + ".txt", **kwargs)
        mail.send(msg)
