from flask import Flask


def create_app():
    app = Flask(__name__)

    from .routes import main, info
    app.register_blueprint(main)
    app.register_blueprint(info, url_prefix="/info")
    return app
