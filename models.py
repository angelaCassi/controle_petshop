#models.py Definição dos modelos de banco de dados)
from app import db

class Dono(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)
    contato = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Dono {self.nome}>'

class Veterinario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    especialidade = db.Column(db.String(80), nullable=False)
    contato = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Veterinario {self.nome}>'

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especie = db.Column(db.String(80), nullable=False)
    idade = db.Column(db.String(20), nullable=False)
    dono_id = db.Column(db.Integer, db.ForeignKey('dono.id'), nullable=False)
    dono = db.relationship('Dono', backref=db.backref('animais', lazy=True))

    def __repr__(self):
        return f'<Animal {self.especie}>'

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20), nullable=False)
    motivo = db.Column(db.String(120), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    veterinario_id = db.Column(db.Integer, db.ForeignKey('veterinario.id'), nullable=False)

    animal = db.relationship('Animal', backref=db.backref('consultas', lazy=True))
    veterinario = db.relationship('Veterinario', backref=db.backref('consultas', lazy=True))

    def __repr__(self):
        return f'<Consulta {self.data}>'
      
