from flask import Flask, request
from controle import *

app = Flask(__name__)

# Rotas para Donos
@app.route('/donos/criar', methods=['POST'])
def criar_dono():
    dono_obj = Dono(None, None, None, None)
    return dono_obj.CriarDono(request.get_json())

@app.route('/donos', methods=['GET'])
def ver_dono():
    return Dono.VerDono()

@app.route('/donos/editar/<int:cpf>', methods=['PUT'])
def editar_dono(cpf):
    dono_obj = Dono(None, None, None, None)
    return dono_obj.EditarDonoCpf(request.get_json(), cpf)

@app.route('/donos/excluir/<int:cpf>', methods=['DELETE'])
def excluir_dono(cpf):
    dono_obj = Dono(None, None, None, None)
    return dono_obj.ExcluirDono(cpf)

# Rotas para Consultas
@app.route('/consultas/agendar', methods=['POST'])
def agendar_consulta():
    consulta_obj = Consulta(None, None, None)
    dados = request.get_json()
    return consulta_obj.AgendarConsulta(dados['dono'], dados['animal'], dados['data_hora'])

@app.route('/consultas/remarcar/<string:animal>', methods=['PUT'])
def remarcar_consulta(animal):
    consulta_obj = Consulta(None, None, None)
    dados = request.get_json()
    return consulta_obj.RemarcarConsulta(animal, dados['nova_data_hora'])

@app.route('/consultas/excluir/<string:animal>', methods=['DELETE'])
def excluir_consulta(animal):
    consulta_obj = Consulta(None, None, None)
    return consulta_obj.ExcluirConsulta(animal)

# Rotas para Animais
@app.route('/animais', methods=['GET'])
def ver_animais():
    dono_obj = Dono(None, None, None, None)
    return dono_obj.VerAnimais()

@app.route('/animais/adicionar', methods=['POST'])
def adicionar_animal():
    dono_obj = Dono(None, None, None, None)
    dados = request.get_json()
    return dono_obj.AdicionarAnimal(dados['especie'], dados['nome'])

@app.route('/animais/excluir/<int:id>', methods=['DELETE'])
def excluir_animal(id):
    dono_obj = Dono(None, None, None, None)
    return dono_obj.ExcluirAnimal(id)

# Rotas para Produtos
@app.route('/produtos', methods=['GET'])
def ver_produtos():
    produto_obj = Produtos(None, None, None)
    return produto_obj.VerProdutos()

@app.route('/produtos/adicionar', methods=['POST'])
def adicionar_produto():
    produto_obj = Produtos(None, None, None)
    return produto_obj.AdicionarProduto(request.get_json())

@app.route('/produtos/excluir/<int:codigo>', methods=['DELETE'])
def excluir_produto(codigo):
    produto_obj = Produtos(None, None, None)
    return produto_obj.ExcluirAnimal(codigo)

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
