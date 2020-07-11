from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD

app = Flask(__name__)
app.config['SECRET_KEY'] = '1e316015f3090e2bcf7f1e2e6deaf173'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kngfshr.reset@gmail.com'
app.config['MAIL_PASSWORD'] = '5EEqdyE3%kB@a#6fYa8E'
mail = Mail(app)

from flasksite import routes
=======
from flask_misaka import Misaka

from flasksite.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    md = Misaka(tables=True, hard_wrap=True)
    app = Flask(__name__)
    md.init_app(app)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flasksite.errors.handlers import errors
    from flasksite.users.routes import users
    from flasksite.posts.routes import posts
    from flasksite.main.routes import main
    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
>>>>>>> 5df6187... First commit
