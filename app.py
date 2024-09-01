#Este arquivo é responsável por configurar o aplicativo Flask, registrar as rotas e iniciar a aplicação.
#Importa a configuração do config.py e inicializa o aplicativo Flask com essas configurações.
from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)

# Inicialização do banco de dados
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Importar e registrar as rotas
    from routes import init_routes
    init_routes(app)

    # Criar o banco de dados
    with app.app_context():
        db.create_all()

    return app

# Executar a aplicação
if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, host='localhost', debug=True)
    
