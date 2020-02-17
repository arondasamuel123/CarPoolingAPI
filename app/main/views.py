from flask import jsonify

from . import main

@main.route("/hello")
def hello():
    return jsonify({'message': 'hello world'})