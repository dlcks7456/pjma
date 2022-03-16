from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown
import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트
    from .views import main_views, project_views, auth_views, dashboard_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(project_views.bp)
    app.register_blueprint(dashboard_views.bp)

    # 필터
    from .filter import format_datetime, checked,country_cnt, country_name_list, country_only_cnt, comma_number
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['checked'] = checked
    app.jinja_env.filters['country_cnt'] = country_cnt
    app.jinja_env.filters['country_only_cnt'] = country_only_cnt
    app.jinja_env.filters['country_name_list'] = country_name_list
    app.jinja_env.filters['comma_number'] = comma_number


    # markdown
    Markdown(app, extensions=['nl2br', 'fenced_code'])


    return app