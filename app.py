import os

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from models import db  # usamos o db definido em models.py


def create_app():
    app = Flask(__name__)

    # Segredo da sessão (pode vir do .env)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret")

    # Proxy fix (pra deploy futuro, não atrapalha em local)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Config do banco
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///teleacolhe.db"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    # Inicializa o SQLAlchemy com esse app
    db.init_app(app)

    # Importa e registra as rotas (blueprint)
    from routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Cria as tabelas
    with app.app_context():
        db.create_all()

    return app


# Instância usada pelo servidor / debug
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
