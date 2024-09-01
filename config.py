#Define a configuração do Flask e do SQLAlchemy.
print("Config.py is being read correctly.")
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///clinica.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
