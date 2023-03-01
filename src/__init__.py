
from flask import Flask, render_template
from os import path
from .common.config import common_config
from .database.database_instance import db
from .modules.user_module import user_bp
from flask_jwt_extended import JWTManager
from .modules.problem_module import problem_bp

def create_app():
    template_dir = path.dirname(path.abspath(path.dirname(__file__)))
    template_dir = path.join(template_dir, 'src', 'templates')
    
    app = Flask(__name__, instance_relative_config=True, template_folder = template_dir)


        # set up database URI based on the environment
    if app.config['ENV'] == 'development':
        app.config.from_mapping(
            SECRET_KEY=common_config.SECRET_KEY,
            SQLALCHEMY_DATABASE_URI=common_config.SQLALCHEMY_DB_URI_DEV,
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=common_config.JWT_SECRET_KEY
        )
    elif app.config['ENV'] == 'production':
        app.config.from_mapping(
            SECRET_KEY=common_config.SECRET_KEY,
            SQLALCHEMY_DATABASE_URI=common_config.SQLALCHEMY_DB_URI_PROD,
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=common_config.JWT_SECRET_KEY
        )
    elif app.config['ENV'] == 'testing':
        app.config.from_mapping(
            SECRET_KEY=common_config.SECRET_KEY,
            SQLALCHEMY_DATABASE_URI=common_config.SQLALCHEMY_DB_URI_TEST,
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=common_config.JWT_SECRET_KEY
        )
    else:
        raise ValueError(f"Unknown environment: {app.config['ENV']}")
    # ensure the instance folder exists
    

    
    db.app = app
    db.init_app(app)
    JWTManager(app)
    
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(user_bp)
    app.register_blueprint(problem_bp)
    
    
    @app.get("/")
    def say_hello():
        return render_template('index.html')
    
    
    
    return app
