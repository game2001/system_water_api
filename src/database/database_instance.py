
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from ..modules.user_module.models import UserModel
from ..modules.problem_module.models import ProblemModel

