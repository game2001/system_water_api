
from flask import Blueprint

problem_bp = Blueprint('problem', __name__, url_prefix='/problems')

# import view to register them with the blueprint
from . import views