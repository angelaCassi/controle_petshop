#Este arquivo é responsável por configurar o aplicativo Flask, registrar as rotas e iniciar a aplicação.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Inicializa o aplicativo e o banco de dados
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Importa e inicializa as rotas
    from routes import init_routes
    init_routes(app)

    with app.app_context():
        db.create_all()  # Cria as tabelas do banco de dados

    return app
    
