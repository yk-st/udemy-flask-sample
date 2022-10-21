from flask import Blueprint,request

landing = Blueprint('landing', 
        __name__, 
        url_prefix='/')

@landing.route('/')
def index():
        print(request.headers)
        return "hello world"
