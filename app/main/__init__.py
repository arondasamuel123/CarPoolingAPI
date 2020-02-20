from flask import Blueprint

main = Blueprint('main', __name__)

from . import errors, views_car, views_user, views_workspace