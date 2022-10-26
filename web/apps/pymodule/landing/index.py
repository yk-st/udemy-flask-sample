from flask import Blueprint,request
from apps.app import db, app

landing = Blueprint('landing', 
        __name__, 
        url_prefix='/')

@landing.route('/')
def index():
        print(request.headers)
        return "hello world"

@app.route("/sitemap.xml")
def sitemap():
    return app.send_static_file("sitemap.xml")

@app.route("/robots.txt")
def robots():
    return app.send_static_file("robots.txt")