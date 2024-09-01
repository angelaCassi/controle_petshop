#Este arquivo define os modelos do banco de dados.
#Este arquivo define as rotas da API e importa os modelos necessários.
from flask import request, jsonify
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


def init_routes(app):
    @app.route('/dono', methods=['POST'])
    def adicionar_dono():
        data = request.json
        novo_dono = Dono(nome=data['nome'], endereco=data['endereco'], contato=data['contato'])
        db.session.add(novo_dono)
        db.session.commit()
        return jsonify({'message': 'Dono adicionado com sucesso!'}), 201

    @app.route('/animais', methods=['GET'])
    def obter_animais():
        animais = Animal.query.all()
        return jsonify([{'id': animal.id, 'especie': animal.especie, 'idade': animal.idade, 'dono': animal.dono.nome} for animal in animais])

    @app.route('/animais', methods=['POST'])
    def adicionar_animal():
        data = request.json
        dono = Dono.query.get(data['dono_id'])
        if not dono:
            return jsonify({'error': 'Dono não encontrado'}), 404

        novo_animal = Animal(especie=data['especie'], idade=data['idade'], dono=dono)
        db.session.add(novo_animal)
        db.session.commit()
        return jsonify({'message': 'Animal adicionado com sucesso!'}), 201

    @app.route('/animais/<int:id>', methods=['DELETE'])
    def remover_animal(id):
        animal = Animal.query.get(id)
        if not animal:
            return jsonify({'error': 'Animal não encontrado'}), 404

        db.session.delete(animal)
        db.session.commit()
        return jsonify({'message': 'Animal removido com sucesso!'}), 200

    @app.route('/veterinarios', methods=['POST'])
    def adicionar_veterinario():
        data = request.json
        novo_veterinario = Veterinario(nome=data['nome'], especialidade=data['especialidade'], contato=data['contato'])
        db.session.add(novo_veterinario)
        db.session.commit()
        return jsonify({'message': 'Veterinário adicionado com sucesso!'}), 201

    @app.route('/veterinarios/<int:id>', methods=['DELETE'])
    def remover_veterinario(id):
        veterinario = Veterinario.query.get(id)
        if not veterinario:
            return jsonify({'error': 'Veterinário não encontrado'}), 404

        db.session.delete(veterinario)
        db.session.commit()
        return jsonify({'message': 'Veterinário removido com sucesso!'}), 200

    @app.route('/consultas', methods=['POST'])
    def agendar_consulta():
        data = request.json
        animal = Animal.query.get(data['animal_id'])
        veterinario = Veterinario.query.get(data['veterinario_id'])

        if not animal or not veterinario:
            return jsonify({'error': 'Animal ou Veterinário não encontrado'}), 404

        nova_consulta = Consulta(data=data['data'], motivo=data['motivo'], animal=animal, veterinario=veterinario)
        db.session.add(nova_consulta)
        db.session.commit()
        return jsonify({'message': 'Consulta agendada com sucesso!'}), 201

    @app.route('/consultas/<int:id>', methods=['DELETE'])
    def remover_consulta(id):
        consulta = Consulta.query.get(id)
        if not consulta:
            return jsonify({'error': 'Consulta não encontrada'}), 404

        db.session.delete(consulta)
        db.session.commit()
        return jsonify({'message': 'Consulta removida com sucesso!'}), 200
