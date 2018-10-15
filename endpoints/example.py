from flask import Blueprint

hello = Blueprint("hello", "hello", url_prefix="/hello-world")

@hello.route('/')
def hello_world():
    return 'Hello World!'
