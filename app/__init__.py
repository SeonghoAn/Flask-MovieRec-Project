from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from app import config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def page_not_found(e):
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    from .controller import main_controller, register_controller, user_controller
    app.register_blueprint(main_controller.bp)
    app.register_blueprint(register_controller.bp)
    app.register_blueprint(user_controller.bp)
    app.register_error_handler(404, page_not_found)

    return app