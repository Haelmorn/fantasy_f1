from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from fantasyf1.config import Config
from flask_caching import Cache
from flask_heroku import Heroku


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
heroku = Heroku()

mail=Mail()
cache = Cache(config={'CACHE_TYPE': 'simple'})


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    heroku.init_app(app)

    from fantasyf1.users.routes import users
    from fantasyf1.posts.routes import posts
    from fantasyf1.main.routes import main
    from fantasyf1.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts) 
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
