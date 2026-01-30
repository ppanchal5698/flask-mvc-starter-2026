#!/usr/bin/env python3
"""
Flask Project Structure Generator (Fixed & Optimized)
Creates a complete, production-ready Flask application.
Usage: python generate_flask_project.py [project_name]
"""

import sys
from pathlib import Path


def generate_flask_project(project_name="myflaskapp"):
    """Generate complete Flask project structure"""

    base = Path(project_name)
    print(f"🚀 Generating Flask project: {project_name}\n")

    # 1. CREATE DIRECTORY STRUCTURE
    print("📁 Creating directories...")
    directories = [
        "app/core", "app/middleware", "app/models", "app/routes",
        "app/schemas", "app/services", "app/utils", "app/decorators",
        "app/validators", "app/static/css", "app/static/js", "app/static/images",
        "app/templates/errors", "tests/unit", "tests/integration",
        "migrations", "docs", "logs"
    ]

    for directory in directories:
        (base / directory).mkdir(parents=True, exist_ok=True)

    # 2. CREATE CORE FILES
    print("⚙️  Creating core application files...")

    # app/__init__.py
    (base / "app/__init__.py").write_text('''from flask import Flask
from app.core.config import config
from app.core.extensions import init_extensions

def create_app(config_name='development'):
    app = Flask(__name__)

    if config_name not in config:
        config_name = 'default'

    app.config.from_object(config[config_name])
    init_extensions(app)

    # Register Blueprints
    from app.routes import main, api, auth
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp, url_prefix='/api')
    app.register_blueprint(auth.bp, url_prefix='/auth')

    return app
''', encoding="utf-8")

    # app/core/config.py
    (base / "app/core/__init__.py").write_text("", encoding="utf-8")
    (base / "app/core/config.py").write_text('''import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
''', encoding="utf-8")

    # app/core/extensions.py
    (base / "app/core/extensions.py").write_text('''from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
''', encoding="utf-8")

    # 3. CREATE MODELS
    print("📊 Creating models...")
    (base / "app/models/__init__.py").write_text("from app.models.user import User", encoding="utf-8")
    (base / "app/models/user.py").write_text('''from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.core.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
''', encoding="utf-8")

    # 4. CREATE ROUTES
    print("🛣️  Creating routes...")
    (base / "app/routes/__init__.py").write_text("", encoding="utf-8")

    # Main routes
    (base / "app/routes/main.py").write_text('''from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/health')
def health():
    return {'status': 'healthy'}, 200
''', encoding="utf-8")

    # API routes
    (base / "app/routes/api.py").write_text('''from flask import Blueprint, jsonify

bp = Blueprint('api', __name__)

@bp.route('/items')
def get_items():
    return jsonify({'items': ['item1', 'item2']})
''', encoding="utf-8")

    # Auth routes
    (base / "app/routes/auth.py").write_text('''from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    # TODO: Replace with actual database lookup and password check
    if username == "admin" and password == "secret":
        token = create_access_token(identity=username)
        return jsonify({'access_token': token}), 200

    return jsonify({"msg": "Bad username or password"}), 401
''', encoding="utf-8")

    # 5. CREATE SERVICES & HELPERS
    print("🔧 Creating services...")
    (base / "app/services/__init__.py").write_text("", encoding="utf-8")
    (base / "app/decorators/__init__.py").write_text("", encoding="utf-8")
    (base / "app/schemas/__init__.py").write_text("", encoding="utf-8")
    (base / "app/utils/__init__.py").write_text("", encoding="utf-8")
    (base / "app/validators/__init__.py").write_text("", encoding="utf-8")
    (base / "app/middleware/__init__.py").write_text("", encoding="utf-8")

    # 6. CREATE TEMPLATES
    print("🎨 Creating templates...")
    (base / "app/templates/base.html").write_text('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask App{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav><h1>Flask App</h1></nav>
    <main>{% block content %}{% endblock %}</main>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
''', encoding="utf-8")

    (base / "app/templates/index.html").write_text('''{% extends "base.html" %}
{% block content %}
<div class="container">
    <h1>Welcome to Flask!</h1>
    <p>Modern Flask application with production best practices.</p>
</div>
{% endblock %}
''', encoding="utf-8")

    # 7. CREATE STATIC FILES
    (base / "app/static/css/style.css").write_text('''* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; background: #f4f4f9; color: #333; }
nav { background: #007bff; color: white; padding: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
main { max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
.container { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
''', encoding="utf-8")

    (base / "app/static/js/main.js").write_text('''console.log('Flask app loaded');
''', encoding="utf-8")

    # 8. CREATE TESTS
    print("🧪 Creating tests...")
    (base / "tests/__init__.py").write_text("", encoding="utf-8")
    (base / "tests/unit/__init__.py").write_text("", encoding="utf-8")
    (base / "tests/integration/__init__.py").write_text("", encoding="utf-8")

    # conftest.py (Fixed to use TestingConfig)
    (base / "tests/conftest.py").write_text('''import pytest
from app import create_app
from app.core.extensions import db

@pytest.fixture
def app():
    # 'testing' config must exist in app/core/config.py
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
''', encoding="utf-8")

    (base / "tests/integration/test_routes.py").write_text('''def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
''', encoding="utf-8")

    # 9. CREATE CONFIG FILES
    print("📄 Creating configuration files...")

    # requirements.txt (Updated with compatible versions and missing postgres driver)
    (base / "requirements.txt").write_text('''Flask>=3.0.0
Flask-SQLAlchemy>=3.1.1
Flask-Migrate>=4.0.0
Flask-JWT-Extended>=4.6.0
Flask-CORS>=4.0.0
Flask-Limiter>=3.0.0
Flask-Caching>=2.1.0
python-dotenv>=1.0.0
redis>=5.0.0
marshmallow>=3.20.0
gunicorn>=21.0.0
pytest>=8.0.0
pytest-cov>=4.1.0
psycopg2-binary>=2.9.0
''', encoding="utf-8")

    # .env.example
    (base / ".env.example").write_text('''FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=change-this-secret-key
DATABASE_URL=sqlite:///app.db
JWT_SECRET_KEY=change-this-jwt-secret
''', encoding="utf-8")

    # .gitignore
    (base / ".gitignore").write_text('''__pycache__/
*.py[cod]
venv/
.env
*.db
*.sqlite
logs/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
''', encoding="utf-8")

    # run.py
    (base / "run.py").write_text('''#!/usr/bin/env python3
from app import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
''', encoding="utf-8")

    # README.md
    (base / "README.md").write_text(f'''# {project_name.title()}

Modern Flask application structure.

## Quick Start

1. **Setup Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

2. **Run Application**
   ```bash
   flask run
   ```

3. **Run Tests**
   ```bash
   pytest
   ```

## Project Structure

- `app/` - Application code
- `app/core/` - Configuration and extensions
- `app/models/` - Database models
- `app/routes/` - Route blueprints
- `app/services/` - Business logic
- `tests/` - Test files
''', encoding="utf-8")

    print(f"\\n✅ Project '{project_name}' created successfully!")
    print("\\n📖 Next steps:")
    print("   cd", project_name)
    print("   python -m venv venv")
    print("   venv\\\\Scripts\\\\activate  # On Windows")
    print("   pip install -r requirements.txt")
    print("   flask run")


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "myflaskapp"
    generate_flask_project(name)
