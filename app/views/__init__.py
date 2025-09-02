from flask import Blueprint

views_bp = Blueprint('views', __name__, template_folder='../templates')

from . import routes