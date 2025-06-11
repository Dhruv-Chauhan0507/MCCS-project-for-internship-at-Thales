# flask_app/app.py

from flask import Flask
from routes.vault_routes import vault_bp
from routes.user_routes import user_bp
from routes.credentials_routes import credential_bp
from routes.advisor_routes import advisor_bp
from init_db import initialize_all_databases

# Initialize DBs before Flask starts
initialize_all_databases()


def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(vault_bp, url_prefix='/vault')
    app.register_blueprint(credential_bp, url_prefix='/credentials')
    app.register_blueprint(advisor_bp, url_prefix='/advisor')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
