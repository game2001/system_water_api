
from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/users')

# import view to register them with the blueprint
from . import views