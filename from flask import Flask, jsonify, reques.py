from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinica.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Classe Dono (Banco de Dados)
class Dono(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    contato = db.Column(db.String(20), nullable=False)
    
    def atualizar_endereco(self, novo_endereco):
        self.endereco = novo_endereco

    def __str__(self):
        return f'{self.nome}, Contato: {self.contato}'

# Classe Veterinário (Banco de Dados)
class Veterinario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    especialidade = db.Column(db.String(50), nullable=False)
    contato = db.Column(db.String(20), nullable=False)
    
    def __str__(self):
        return f'Dr(a). {self.nome}, Especialidade: {self.especialidade}, Contato: {self.contato}'

# Classe Animal (Banco de Dados)
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especie = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.String(20), nullable=False)
    dono_id = db.Column(db.Integer, db.ForeignKey('dono.id'), nullable=False)
    dono = db.relationship('Dono', backref=db.backref('animais', lazy=True))
    
    def __str__(self):
        return f'Animal: {self.especie}, Idade: {self.idade}, Dono: {self.dono.nome}.'

# Classe Consulta (Banco de Dados)
class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    veterinario_id = db.Column(db.Integer, db.ForeignKey('veterinario.id'), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    motivo = db.Column(db.String(100), nullable=False)
    
    animal = db.relationship('Animal', backref=db.backref('consultas', lazy=True))
    veterinario = db.relationship('Veterinario', backref=db.backref('consultas', lazy=True))

    def remarcar(self, nova_data):
        self.data = nova_data
    
    def __str__(self):
        return f'Consulta para {self.animal.especie} com {self.veterinario.nome} em {self.data} - Motivo: {self.motivo}'

# Inicialização do Banco de Dados
with app.app_context():
    db.create_all()

# Rotas Flask

# Rota para obter a lista de animais
@app.route('/animais', methods=['GET'])
def obter_animais():
    animais = Animal.query.all()
    return jsonify([str(animal) for animal in animais])

# Rota para obter a lista de veterinários
@app.route('/veterinarios', methods=['GET'])
def obter_veterinarios():
    veterinarios = Veterinario.query.all()
    return jsonify([str(veterinario) for veterinario in veterinarios])

# Rota para agendar uma nova consulta
@app.route('/consultas', methods=['POST'])
def agendar_consulta():
    data = request.json
    animal_id = data.get('animalId')
    veterinario_nome = data.get('veterinarioNome')
    data_consulta = data.get('data')
    motivo = data.get('motivo')
    
    animal = Animal.query.get(animal_id)
    veterinario = Veterinario.query.filter_by(nome=veterinario_nome).first()

    if not animal or not veterinario:
        abort(404, description="Animal ou Veterinário não encontrado.")
    
    nova_consulta = Consulta(animal=animal, veterinario=veterinario, data=data_consulta, motivo=motivo)
    db.session.add(nova_consulta)
    db.session.commit()
    
    return jsonify({'message': 'Consulta agendada com sucesso!'}), 201

# Rota para editar uma consulta
@app.route('/consultas/<int:id>', methods=['PUT'])
def editar_consulta(id):
    consulta = Consulta.query.get(id)
    if not consulta:
        abort(404, description="Consulta não encontrada.")
    
    data = request.json
    nova_data = data.get('data')
    novo_motivo = data.get('motivo')
    
    if nova_data:
        consulta.remarcar(nova_data)
    if novo_motivo:
        consulta.motivo = novo_motivo

    db.session.commit()
    
    return jsonify({'message': 'Consulta atualizada com sucesso!'}), 200

# Rota para deletar uma consulta
@app.route('/consultas/<int:id>', methods=['DELETE'])
def deletar_consulta(id):
    consulta = Consulta.query.get(id)
    if not consulta:
        abort(404, description="Consulta não encontrada.")
    
    db.session.delete(consulta)
    db.session.commit()
    
    return jsonify({'message': 'Consulta deletada com sucesso!'}), 200

# Rota para adicionar um novo animal
@app.route('/animais', methods=['POST'])
def adicionar_animal():
    data = request.json
    especie = data.get('especie')
    idade = data.get('idade')
    dono_id = data.get('donoId')
    
    dono = Dono.query.get(dono_id)
    if not dono:
        abort(404, description="Dono não encontrado.")
    
    novo_animal = Animal(especie=especie, idade=idade, dono=dono)
    db.session.add(novo_animal)
    db.session.commit()
    
    return jsonify({'message': 'Animal adicionado com sucesso!'}), 201

# Rota para deletar um animal
@app.route('/animais/<int:id>', methods=['DELETE'])
def deletar_animal(id):
    animal = Animal.query.get(id)
    if not animal:
        abort(404, description="Animal não encontrado.")
    
    db.session.delete(animal)
    db.session.commit()
    
    return jsonify({'message': 'Animal deletado com sucesso!'}), 200

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
    