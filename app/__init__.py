from flask import Flask, render_template

from app.core.config import config
from app.core.extensions import init_extensions


def create_app(config_name='development'):
    app = Flask(__name__)

    if config_name not in config:
        config_name = 'default'

    app.config.from_object(config[config_name])
    init_extensions(app)

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    # Register Blueprints
    from app.routes import api, auth, main
    from app.routes.swagger import swagger_bp

    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp, url_prefix='/api/v1')
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(swagger_bp, url_prefix='/api')  # Swagger UI at /api/docs

    return app
