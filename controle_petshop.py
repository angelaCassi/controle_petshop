# from flask import Flask, jsonify, request

# app = Flask(__name__)

# Classe Dono
class Dono:
    def __init__(self, nome, endereco, contato):
        self.nome = nome
        self.endereco = endereco
        self.contato = contato

    def atualizar_endereco(self, novo_endereco):
        self.endereco = novo_endereco

    def __str__(self):
        return f'{self.nome}, Contato: {self.contato}'

# Classe Veterinário
class Veterinario:
    def __init__(self, nome, especialidade, contato):
        self.nome = nome
        self.especialidade = especialidade
        self.contato = contato

    def __str__(self):
        return f'Dr(a). {self.nome}, Especialidade: {self.especialidade}, Contato: {self.contato}'

# Classe Consulta
class Consulta:
    def __init__(self, animal, veterinario, data, motivo):
        self.animal = animal
        self.veterinario = veterinario
        self.data = data
        self.motivo = motivo

    def remarcar(self, nova_data):
        self.data = nova_data

    def __str__(self):
        return f'Consulta para {self.animal.especie} com {self.veterinario.nome} em {self.data} - Motivo: {self.motivo}'

# Classe Serviço
class Servico:
    def __init__(self, tipo, preco, duracao):
        self.tipo = tipo
        self.preco = preco
        self.duracao = duracao

    def aplicar_desconto(self, percentual):
        self.preco -= self.preco * (percentual/100)

    def __str__(self):
        return f'Serviço: {self.tipo} Preço: R${self.preco}, Duração: {self.duracao} minutos.'

# Classe Animal
class Animal:
    def __init__(self, id, especie, idade, dono: Dono):
        self.id = id
        self.especie = especie
        self.idade = idade
        self.dono = dono

    def __str__(self):
        return f'Animal: {self.especie}, Idade: {self.idade}, Dono: {self.dono.nome}.'

# Classe ClinicaVeterinaria
class ClinicaVeterinaria:
    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco
        self.veterinarios = []
        self.consultas = []
        self.animais = []

    def adicionar_veterinario(self, veterinario):
        self.veterinarios.append(veterinario)

    def agendar_consulta(self, consulta):
        self.consultas.append(consulta)

    def adicionar_animal(self, animal):
        self.animais.append(animal)

    def listar_animais(self):
        return [str(animal) for animal in self.animais]

    def listar_veterinarios(self):
        return [str(veterinario) for veterinario in self.veterinarios]

    def listar_consultas(self):
        return [str(consulta) for consulta in self.consultas]

    def encontrar_consulta(self, id):
        for consulta in self.consultas:
            if consulta.id == id:
                return consulta
        return None

    def __str__(self):
        return f'Clínica {self.nome}, Endereço: {self.endereco}, Veterinários: {len(self.veterinarios)}'

# Exemplo de instâncias criadas manualmente    
""""" dono1 = Dono('Lucas', 'Rua A, 123', '1111-1111')
dono2 = Dono('Joana', 'Rua B, 231', '2222-2222')
dono3 = Dono('Mario', 'Rua C, 321', '3333-3333')

animal1 = Animal(1, 'Cachorro', '2 anos', dono1)
animal2 = Animal(2, 'Gato', '5 anos', dono2)
animal3 = Animal(3, 'Pato', '1 ano', dono3)

veterinario1 = Veterinario('Dr.João', 'Cachorros', '1111-1111')
veterinario2 = Veterinario('Dra.Lygia', 'Gatos', '8888-8888')
veterinario3 = Veterinario('Dra.Nadia', 'Geral', '6746-8444')

clinica = ClinicaVeterinaria('Clinica Pet+', 'Av.Magalhães, 231')
clinica.adicionar_veterinario(veterinario1)
clinica.adicionar_veterinario(veterinario2)
clinica.adicionar_veterinario(veterinario3)
clinica.adicionar_animal(animal1)
clinica.adicionar_animal(animal2)
clinica.adicionar_animal(animal3)

# Rotas Flask

# Rota para obter a lista de animais
@app.route('/animais', methods=['GET'])
def obter_animais():
    return jsonify(clinica.listar_animais())

# Rota para obter a lista de veterinários
@app.route('/veterinarios', methods=['GET'])
def obter_veterinarios():
    return jsonify(clinica.listar_veterinarios())

# Rota para obter a lista de consultas
@app.route('/consultas', methods=['GET'])
def obter_consultas():
    return jsonify(clinica.listar_consultas())

# Rota para agendar uma nova consulta
@app.route('/consultas', methods=['POST'])
def agendar_consulta():
    data = request.json
    animal_id = data.get('animalId')
    veterinario_nome = data.get('veterinarioNome')
    data_consulta = data.get('data')
    motivo = data.get('motivo')

    animal = next((a for a in clinica.animais if a.id == animal_id), None)
    veterinario = next((v for v in clinica.veterinarios if v.nome == veterinario_nome), None)

    if animal and veterinario:
        nova_consulta = Consulta(animal, veterinario, data_consulta, motivo)
        clinica.agendar_consulta(nova_consulta)
        return jsonify({'message': 'Consulta agendada com sucesso!'}), 201
    else:
        return jsonify({'error': 'Animal ou Veterinário não encontrado'}), 404

# Rota para editar uma consulta
@app.route('/consultas/<int:id>', methods=['PUT'])
def editar_consulta(id):
    consulta = clinica.encontrar_consulta(id)
    if not consulta:
        return jsonify({'error': 'Consulta não encontrada'}), 404

    data = request.json
    nova_data = data.get('data')
    novo_motivo = data.get('motivo')

    if nova_data:
        consulta.remarcar(nova_data)
    if novo_motivo:
        consulta.motivo = novo_motivo

    return jsonify({'message': 'Consulta atualizada com sucesso!'}), 200

# Rota para remover uma consulta
@app.route('/consultas/<int:id>', methods=['DELETE'])
def remover_consulta(id):
    consulta = clinica.encontrar_consulta(id)
    if not consulta:
        return jsonify({'error': 'Consulta não encontrada'}), 404
       


    clinica.consultas.remove(consulta)
    return jsonify({'message': 'Consulta removida com sucesso!'}), 200

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)

    """"" 
