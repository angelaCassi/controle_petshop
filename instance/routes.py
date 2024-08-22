# routes.py
from flask import jsonify, request
from models import * # ClinicaVeterinaria, Consulta,

# Instâncias criadas manualmente

dono1 = Dono('Lucas', 'Rua A, 123', '1111-1111')
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

def init_routes(app):
    @app.route('/animais', methods=['GET'])
    def obter_animais():
        return jsonify(clinica.listar_animais())

    @app.route('/veterinarios', methods=['GET'])
    def obter_veterinarios():
        return jsonify(clinica.listar_veterinarios())

    @app.route('/consultas', methods=['GET'])
    def obter_consultas():
        return jsonify(clinica.listar_consultas())

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

    @app.route('/consultas/<int:id>', methods=['DELETE'])
    def remover_consulta(id):
        consulta = clinica.encontrar_consulta(id)
        if not consulta:
            return jsonify({'error': 'Consulta não encontrada'}), 404

        clinica.consultas.remove(consulta)
        return jsonify({'message': 'Consulta removida com sucesso!'}), 200